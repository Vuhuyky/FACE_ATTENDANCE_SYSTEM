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