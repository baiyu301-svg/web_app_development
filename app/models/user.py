from app.models import get_db_connection

class User:
    @staticmethod
    def create(email, password_hash):
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

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get_by_email(email):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def update_credit_score(user_id, delta):
        conn = get_db_connection()
        conn.execute(
            'UPDATE users SET credit_score = credit_score + ? WHERE id = ?',
            (delta, user_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(user_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
