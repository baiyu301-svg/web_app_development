from app.models import get_db_connection

class ChatMessage:
    @staticmethod
    def create(match_id, sender_id, content):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO chat_messages (match_id, sender_id, content)
               VALUES (?, ?, ?)''',
            (match_id, sender_id, content)
        )
        conn.commit()
        message_id = cursor.lastrowid
        conn.close()
        return message_id

    @staticmethod
    def get_by_match_id(match_id):
        conn = get_db_connection()
        messages = conn.execute(
            'SELECT * FROM chat_messages WHERE match_id = ? ORDER BY created_at ASC',
            (match_id,)
        ).fetchall()
        conn.close()
        return [dict(m) for m in messages]
