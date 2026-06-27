SELECT * FROM schedules;

UPDATE schedules
SET start_time = '00:00',
    end_time   = '18:35'
WHERE id = 1;

	SELECT
		id,
		section_id,
		session_date,
		is_active
	FROM attendance_sessions
	ORDER BY id DESC;

UPDATE schedules
SET end_time='18:46'
WHERE id=1;

UPDATE schedules
SET weekday = 3,
    start_time = '18:53',
    end_time = '18:59'
WHERE section_id = 2;

INSERT INTO enrollments
(student_id, section_id)
VALUES
(1, 2);

INSERT INTO enrollments
(student_id, section_id)
VALUES
(2, 2);

SELECT
    e.student_id,
    s.student_code,
    s.full_name,
    e.section_id
FROM enrollments e
JOIN students s
    ON e.student_id = s.id;




PRAGMA table_info(attendance_sessions);

UPDATE schedules
SET weekday = 3,
    start_time = '22:41',
    end_time = '22:43'
WHERE section_id = 2;

SELECT * FROM schedules;

DELETE FROM course_sections
WHERE id IN (3,4);

SELECT * FROM course_sections;

UPDATE course_sections
SET section_name = 'CV101-01'
WHERE id = 1;

UPDATE course_sections
SET section_name = 'AI101-01'
WHERE id = 2;

UPDATE students
SET email = 'kyhuyvu@gmail.com'
WHERE id = 4;