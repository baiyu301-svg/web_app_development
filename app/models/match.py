from app.models import get_db_connection

class Match:
    @staticmethod
    def create(wishlist_id_1, wishlist_id_2):
        """
        新增一筆配對成功記錄
        :param wishlist_id_1: 第一筆願望清單 ID
        :param wishlist_id_2: 第二筆願望清單 ID
        :return: 成功回傳 match_id，失敗回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO matches (wishlist_id_1, wishlist_id_2, status)
                   VALUES (?, ?, 'chatting')''',
                (wishlist_id_1, wishlist_id_2)
            )
            conn.commit()
            match_id = cursor.lastrowid
            conn.close()
            return match_id
        except Exception as e:
            print(f"Error in Match.create: {e}")
            return None

    @staticmethod
    def get_all():
        """
        取得所有配對記錄
        :return: dict 列表
        """
        try:
            conn = get_db_connection()
            matches = conn.execute('SELECT * FROM matches').fetchall()
            conn.close()
            return [dict(m) for m in matches]
        except Exception as e:
            print(f"Error in Match.get_all: {e}")
            return []

    @staticmethod
    def get_by_id(match_id):
        """
        取得單筆配對記錄
        :param match_id: 配對記錄 ID
        :return: dict 或 None
        """
        try:
            conn = get_db_connection()
            match = conn.execute('SELECT * FROM matches WHERE id = ?', (match_id,)).fetchone()
            conn.close()
            return dict(match) if match else None
        except Exception as e:
            print(f"Error in Match.get_by_id: {e}")
            return None

    @staticmethod
    def get_user_matches(user_id):
        """
        取得特定使用者參與的所有配對記錄
        :param user_id: 使用者 ID
        :return: dict 列表
        """
        try:
            conn = get_db_connection()
            matches = conn.execute(
                '''SELECT m.* FROM matches m
                   JOIN wishlists w1 ON m.wishlist_id_1 = w1.id
                   JOIN wishlists w2 ON m.wishlist_id_2 = w2.id
                   WHERE w1.user_id = ? OR w2.user_id = ?''',
                (user_id, user_id)
            ).fetchall()
            conn.close()
            return [dict(m) for m in matches]
        except Exception as e:
            print(f"Error in Match.get_user_matches: {e}")
            return []

    @staticmethod
    def update(match_id, data):
        """
        更新配對記錄
        :param match_id: 配對記錄 ID
        :param data: 包含更新欄位的字典
        :return: bool 是否成功
        """
        try:
            conn = get_db_connection()
            set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
            values = list(data.values())
            values.append(match_id)
            
            conn.execute(
                f'UPDATE matches SET {set_clause} WHERE id = ?',
                values
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error in Match.update: {e}")
            return False

    @staticmethod
    def update_status(match_id, new_status):
        """
        快速更新配對記錄狀態
        :param match_id: 配對記錄 ID
        :param new_status: 新狀態 ('chatting', 'completed', 'cancelled')
        :return: bool 是否成功
        """
        return Match.update(match_id, {'status': new_status})

    @staticmethod
    def delete(match_id):
        """
        刪除配對記錄
        :param match_id: 配對記錄 ID
        :return: bool 是否成功
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM matches WHERE id = ?', (match_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error in Match.delete: {e}")
            return False
