from app.models import get_db_connection

class Course:
    @staticmethod
    def create(course_code, name, department=None, instructor=None, credits=0):
        """
        新增一筆課程記錄
        :param course_code: 課程代碼
        :param name: 課程名稱
        :param department: 系所
        :param instructor: 授課教師
        :param credits: 學分數
        :return: 成功回傳 course_id，失敗回傳 None
        """
        try:
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
        except Exception as e:
            print(f"Error in Course.create: {e}")
            return None

    @staticmethod
    def get_all():
        """
        取得所有課程記錄
        :return: dict 列表
        """
        try:
            conn = get_db_connection()
            courses = conn.execute('SELECT * FROM courses').fetchall()
            conn.close()
            return [dict(c) for c in courses]
        except Exception as e:
            print(f"Error in Course.get_all: {e}")
            return []

    @staticmethod
    def get_by_id(course_id):
        """
        取得單筆課程記錄
        :param course_id: 課程 ID
        :return: dict 或 None
        """
        try:
            conn = get_db_connection()
            course = conn.execute('SELECT * FROM courses WHERE id = ?', (course_id,)).fetchone()
            conn.close()
            return dict(course) if course else None
        except Exception as e:
            print(f"Error in Course.get_by_id: {e}")
            return None

    @staticmethod
    def update(course_id, data):
        """
        更新課程記錄
        :param course_id: 課程 ID
        :param data: 包含更新欄位的字典
        :return: bool 是否成功
        """
        try:
            conn = get_db_connection()
            set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
            values = list(data.values())
            values.append(course_id)
            
            conn.execute(
                f'UPDATE courses SET {set_clause} WHERE id = ?',
                values
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error in Course.update: {e}")
            return False

    @staticmethod
    def delete(course_id):
        """
        刪除課程記錄
        :param course_id: 課程 ID
        :return: bool 是否成功
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM courses WHERE id = ?', (course_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error in Course.delete: {e}")
            return False
