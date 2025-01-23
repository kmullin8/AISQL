import json
from openai import OpenAI
import os
import sqlite3
from time import time

print("Running db_bot.py!")

fdir = os.path.dirname(__file__)
def getPath(fname):
    return os.path.join(fdir, fname)

# SQLITE
sqliteDbPath = getPath("aidb.sqlite")
setupSqlPath = getPath("setup.sql")
setupSqlDataPath = getPath("setupData.sql")

# Erase previous db
if os.path.exists(sqliteDbPath):
    os.remove(sqliteDbPath) 

sqliteCon = sqlite3.connect(sqliteDbPath) # create new db
sqliteCursor = sqliteCon.cursor()
with (
        open(setupSqlPath) as setupSqlFile,
        open(setupSqlDataPath) as setupSqlDataFile
    ):

    setupSqlScript = setupSqlFile.read()
    setupSQlDataScript = setupSqlDataFile.read()

sqliteCursor.executescript(setupSqlScript) # setup tables and keys
sqliteCursor.executescript(setupSQlDataScript) # setup tables and keys

def runSql(query):
    result = sqliteCursor.execute(query).fetchall()
    return result

# OPENAI
configPath = getPath("config.json")
#print("0 ", configPath)
with open(configPath) as configFile:
    config = json.load(configFile)

openAiClient = OpenAI(api_key = config["openaiKey"])

def getChatGptResponse(content):
    stream = openAiClient.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": content}],
        stream=True,  # Enables streaming response
    )

    responseList = []
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            word = chunk.choices[0].delta.content
            responseList.append(word)
            #print(word, end="", flush=True)  # Print each word in real-time

    return "".join(responseList)



# strategies
commonSqlOnlyRequest = " Give me a sqlite select statement that answers the question. Only respond with sqlite syntax. If there is an error do not expalin it!"
strategies = {
    "zero_shot": setupSqlScript + commonSqlOnlyRequest,
    "single_domain_double_shot": (setupSqlScript + 
                   " Here is an example:\nFind members who have never attended a class? " +
                   " \nSELECT m.member_id, m.name\nFROM member m\nLEFT JOIN attendance a ON m.member_id = a.member_id\nWHERE a.member_id IS NULL;\n " +
                   commonSqlOnlyRequest)
}

questions = [
    "   Which are the most active members based on class attendance?",
    "   Which members have attended multiple different classes?",
    "   Which trainers have the most personal training sessions?",
    "   What are the top 3 most attended classes?",
    "   Which members have personal training sessions scheduled?",
    "   Who has more than one personal training session with the same trainer?",
    "   Which members do not have an email or phone number on file?",
    "   Are there any trainers who have not been assigned to a class?"
]

def sanitizeForJustSql(value):
    gptStartSqlMarker = "```sql"
    gptEndSqlMarker = "```"

    # Extract only the SQL content
    if gptStartSqlMarker in value:
        value = value.split(gptStartSqlMarker)[1]
    if gptEndSqlMarker in value:
        value = value.split(gptEndSqlMarker)[0]

    # Add a tab at the beginning of each line
    value = "\n".join("\t" + line for line in value.strip().split("\n"))

    return value

for strategy in strategies:
    responses = {"strategy": strategy, "prompt_prefix": strategies[strategy]}
    questionResults = []
    for question in questions:
        print("Question:\n", question)
        error = "None"
        sqlSyntaxResponse = ""
        queryRawResponse = ""
        friendlyResponse = ""

        try:
            sqlSyntaxResponse = getChatGptResponse(strategies[strategy] + " " + question)
            sqlSyntaxResponse = sanitizeForJustSql(sqlSyntaxResponse)
            print("SQL: \n", sqlSyntaxResponse)

            queryRawResponse = str(runSql(sqlSyntaxResponse))
            print("Raw Response:\n", "  ", queryRawResponse)

            friendlyResultsPrompt = f'I asked a question "{question}" and the response was "{queryRawResponse}" here is the schema this data was located in:"{setupSqlScript}". Please, just give a concise response in a more friendly way? Please do not give any other suggests or chatter.'
            friendlyResponse = getChatGptResponse(friendlyResultsPrompt)
            print("Response:\n", "  ", friendlyResponse, "\n\n")
        except Exception as err:
            error = str(err)
            print("Error:\n", err)

        questionResults.append({
            "question": question,
            "sql": sqlSyntaxResponse,
            "queryRawResponse": queryRawResponse,
            "friendlyResponse": friendlyResponse,
            "error": error
        })

    responses["questionResults"] = questionResults

    with open(getPath(f"response_{strategy}_{time()}.json"), "w") as outFile:
        json.dump(responses, outFile, indent=2)
            

sqliteCursor.close()
sqliteCon.close()
print("Done!")