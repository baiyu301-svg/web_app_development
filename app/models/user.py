from app.models import get_db_connection

class User:
    @staticmethod
    def create(email, password_hash):
        """
        新增一筆使用者記錄
        :param email: 使用者信箱
        :param password_hash: 加密後的密碼
        :return: 成功回傳 user_id，失敗回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (email, password_hash) VALUES (?, ?)',
                (email, password_hash)
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except Exception as e:
            print(f"Error in User.create: {e}")
            return None

    @staticmethod
    def get_all():
        """
        取得所有使用者記錄
        :return: dict 列表
        """
        try:
            conn = get_db_connection()
            users = conn.execute('SELECT * FROM users').fetchall()
            conn.close()
            return [dict(u) for u in users]
        except Exception as e:
            print(f"Error in User.get_all: {e}")
            return []

    @staticmethod
    def get_by_id(user_id):
        """
        取得單筆使用者記錄
        :param user_id: 使用者 ID
        :return: dict 或 None
        """
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            conn.close()
            return dict(user) if user else None
        except Exception as e:
            print(f"Error in User.get_by_id: {e}")
            return None

    @staticmethod
    def get_by_email(email):
        """
        根據 Email 取得使用者記錄
        :param email: 使用者 Email
        :return: dict 或 None
        """
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            conn.close()
            return dict(user) if user else None
        except Exception as e:
            print(f"Error in User.get_by_email: {e}")
            return None

    @staticmethod
    def update(user_id, data):
        """
        更新使用者記錄
        :param user_id: 使用者 ID
        :param data: 包含更新欄位的字典 (例如 {'credit_score': 105})
        :return: bool 是否成功
        """
        try:
            conn = get_db_connection()
            set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
            values = list(data.values())
            values.append(user_id)
            
            conn.execute(
                f'UPDATE users SET {set_clause} WHERE id = ?',
                values
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error in User.update: {e}")
            return False

    @staticmethod
    def update_credit_score(user_id, delta):
        """
        更新使用者信用分數
        :param user_id: 使用者 ID
        :param delta: 增減數值
        :return: bool 是否成功
        """
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE users SET credit_score = credit_score + ? WHERE id = ?',
                (delta, user_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error in User.update_credit_score: {e}")
            return False

    @staticmethod
    def delete(user_id):
        """
        刪除使用者記錄
        :param user_id: 使用者 ID
        :return: bool 是否成功
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error in User.delete: {e}")
            return False
