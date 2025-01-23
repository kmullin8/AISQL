-- Gym Membership System Schema

CREATE TABLE member (
    member_id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    date_joined DATE NOT NULL,
    membership_id INTEGER NOT NULL,
    FOREIGN KEY (membership_id) REFERENCES membership (membership_id)
);


CREATE TABLE trainer (
    trainer_id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    specialty VARCHAR(50),
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15)
);

CREATE TABLE membership (
    membership_id INTEGER PRIMARY KEY,
    type VARCHAR(20) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    duration_months INTEGER NOT NULL
);

CREATE TABLE class (
    class_id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    trainer_id INTEGER NOT NULL,
    schedule VARCHAR(50),
    FOREIGN KEY (trainer_id) REFERENCES trainer (trainer_id)
);

CREATE TABLE attendance (
    attendance_id INTEGER PRIMARY KEY,
    member_id INTEGER NOT NULL,
    class_id INTEGER NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (member_id) REFERENCES member (member_id),
    FOREIGN KEY (class_id) REFERENCES class (class_id)
);

CREATE TABLE equipment (
    equipment_id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    last_maintenance DATE NOT NULL
);

CREATE TABLE session (
    session_id INTEGER PRIMARY KEY,
    member_id INTEGER NOT NULL,
    trainer_id INTEGER NOT NULL,
    session_date DATE NOT NULL,
    FOREIGN KEY (member_id) REFERENCES member (member_id),
    FOREIGN KEY (trainer_id) REFERENCES trainer (trainer_id)
);