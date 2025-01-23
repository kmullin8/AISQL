INSERT INTO membership (membership_id, type, price, duration_months) VALUES
(1, 'Monthly', 50.00, 1),
(2, 'Quarterly', 135.00, 3),
(3, 'Annual', 480.00, 12);

INSERT INTO trainer (trainer_id, name, specialty, email, phone) VALUES
(1, 'Alice Johnson', 'Strength Training', 'alice.johnson@example.com', '123-456-7890'),
(2, 'Bob Smith', 'Yoga', 'bob.smith@example.com', '234-567-8901');

INSERT INTO member (member_id, name, email, phone, date_joined, membership_id) VALUES
(1, 'John Doe', 'john.doe@example.com', '345-678-9012', '2023-01-10', 1),
(2, 'Jane Smith', 'jane.smith@example.com', '456-789-0123', '2023-02-15', 2),
(3, 'Josh Allen', 'josh.allen@example.com', '907-774-5222', '2023-03-120', 2);

INSERT INTO class (class_id, name, trainer_id, schedule) VALUES
(1, 'HIIT Workout', 1, 'Monday 6 PM'),
(2, 'Morning Yoga', 2, 'Wednesday 8 AM');

INSERT INTO attendance (attendance_id, member_id, class_id, date) VALUES
(1, 1, 1, '2024-01-05'),
(2, 1, 2, '2024-01-05'),
(3, 2, 2, '2024-01-10');

INSERT INTO equipment (equipment_id, name, last_maintenance) VALUES
(1, 'Treadmill', '2023-12-01'),
(2, 'Bench Press', '2023-11-15');

INSERT INTO session (session_id, member_id, trainer_id, session_date) VALUES
(1, 1, 1, '2024-01-12'),
(2, 2, 2, '2024-01-12'),
(3, 2, 2, '2024-01-15');
