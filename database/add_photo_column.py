from database.connection import get_connection


def add_photo_column():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "PRAGMA table_info(students)"
    )

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    if "photo_path" not in columns:

        cursor.execute(
            "ALTER TABLE students ADD COLUMN photo_path TEXT"
        )

        conn.commit()

        print("Added 'photo_path' column to 'students' table.")

    else:

        print("'photo_path' column already exists - nothing to do.")

    conn.close()


if __name__ == "__main__":

    add_photo_column()