from app.models import get_db_connection

class Course:
    @staticmethod
    def create(course_code, name, department=None, instructor=None, credits=0):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO courses (course_code, name, department, instructor, credits)
               VALUES (?, ?, ?, ?, ?)''',
            (course_code, name, department, instructor, credits)
        )
        conn.commit()
        course_id = cursor.lastrowid
        conn.close()
        return course_id

    @staticmethod
    def get_by_id(course_id):
        conn = get_db_connection()
        course = conn.execute('SELECT * FROM courses WHERE id = ?', (course_id,)).fetchone()
        conn.close()
        return dict(course) if course else None

    @staticmethod
    def get_all():
        conn = get_db_connection()
        courses = conn.execute('SELECT * FROM courses').fetchall()
        conn.close()
        return [dict(c) for c in courses]

    @staticmethod
    def delete(course_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM courses WHERE id = ?', (course_id,))
        conn.commit()
        conn.close()
