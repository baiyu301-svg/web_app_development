from app.models import get_db_connection

class ChatMessage:
    @staticmethod
    def create(match_id, sender_id, content):
        """
        新增一筆聊天訊息記錄
        :param match_id: 配對記錄 ID
        :param sender_id: 發送者 ID
        :param content: 訊息內容
        :return: 成功回傳 message_id，失敗回傳 None
        """
        try:
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
        except Exception as e:
            print(f"Error in ChatMessage.create: {e}")
            return None

    @staticmethod
    def get_all():
        """
        取得所有聊天訊息記錄
        :return: dict 列表
        """
        try:
            conn = get_db_connection()
            messages = conn.execute('SELECT * FROM chat_messages').fetchall()
            conn.close()
            return [dict(m) for m in messages]
        except Exception as e:
            print(f"Error in ChatMessage.get_all: {e}")
            return []

    @staticmethod
    def get_by_id(message_id):
        """
        取得單筆聊天訊息記錄
        :param message_id: 訊息 ID
        :return: dict 或 None
        """
        try:
            conn = get_db_connection()
            message = conn.execute('SELECT * FROM chat_messages WHERE id = ?', (message_id,)).fetchone()
            conn.close()
            return dict(message) if message else None
        except Exception as e:
            print(f"Error in ChatMessage.get_by_id: {e}")
            return None

    @staticmethod
    def get_by_match_id(match_id):
        """
        取得特定配對記錄的所有聊天訊息（依時間排序）
        :param match_id: 配對記錄 ID
        :return: dict 列表
        """
        try:
            conn = get_db_connection()
            messages = conn.execute(
                'SELECT * FROM chat_messages WHERE match_id = ? ORDER BY created_at ASC',
                (match_id,)
            ).fetchall()
            conn.close()
            return [dict(m) for m in messages]
        except Exception as e:
            print(f"Error in ChatMessage.get_by_match_id: {e}")
            return []

    @staticmethod
    def update(message_id, data):
        """
        更新聊天訊息記錄
        :param message_id: 訊息 ID
        :param data: 包含更新欄位的字典
        :return: bool 是否成功
        """
        try:
            conn = get_db_connection()
            set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
            values = list(data.values())
            values.append(message_id)
            
            conn.execute(
                f'UPDATE chat_messages SET {set_clause} WHERE id = ?',
                values
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error in ChatMessage.update: {e}")
            return False

    @staticmethod
    def delete(message_id):
        """
        刪除聊天訊息記錄
        :param message_id: 訊息 ID
        :return: bool 是否成功
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM chat_messages WHERE id = ?', (message_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error in ChatMessage.delete: {e}")
            return False
