from app.models import get_db_connection

class Wishlist:
    @staticmethod
    def create(user_id, held_course_id, target_course_id):
        """
        新增一筆願望清單記錄
        :param user_id: 建立願望的使用者 ID
        :param held_course_id: 想換出的課程 ID
        :param target_course_id: 想換入的課程 ID
        :return: 成功回傳 wishlist_id，失敗回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO wishlists (user_id, held_course_id, target_course_id, status)
                   VALUES (?, ?, ?, 'pending')''',
                (user_id, held_course_id, target_course_id)
            )
            conn.commit()
            wishlist_id = cursor.lastrowid
            conn.close()
            return wishlist_id
        except Exception as e:
            print(f"Error in Wishlist.create: {e}")
            return None

    @staticmethod
    def get_all():
        """
        取得所有願望清單記錄
        :return: dict 列表
        """
        try:
            conn = get_db_connection()
            wishlists = conn.execute('SELECT * FROM wishlists').fetchall()
            conn.close()
            return [dict(w) for w in wishlists]
        except Exception as e:
            print(f"Error in Wishlist.get_all: {e}")
            return []

    @staticmethod
    def get_by_id(wishlist_id):
        """
        取得單筆願望清單記錄
        :param wishlist_id: 願望清單 ID
        :return: dict 或 None
        """
        try:
            conn = get_db_connection()
            wishlist = conn.execute('SELECT * FROM wishlists WHERE id = ?', (wishlist_id,)).fetchone()
            conn.close()
            return dict(wishlist) if wishlist else None
        except Exception as e:
            print(f"Error in Wishlist.get_by_id: {e}")
            return None

    @staticmethod
    def get_by_user(user_id):
        """
        取得特定使用者的所有願望清單記錄
        :param user_id: 使用者 ID
        :return: dict 列表
        """
        try:
            conn = get_db_connection()
            wishlists = conn.execute('SELECT * FROM wishlists WHERE user_id = ?', (user_id,)).fetchall()
            conn.close()
            return [dict(w) for w in wishlists]
        except Exception as e:
            print(f"Error in Wishlist.get_by_user: {e}")
            return []

    @staticmethod
    def update(wishlist_id, data):
        """
        更新願望清單記錄
        :param wishlist_id: 願望清單 ID
        :param data: 包含更新欄位的字典
        :return: bool 是否成功
        """
        try:
            conn = get_db_connection()
            set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
            values = list(data.values())
            values.append(wishlist_id)
            
            conn.execute(
                f'UPDATE wishlists SET {set_clause} WHERE id = ?',
                values
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error in Wishlist.update: {e}")
            return False

    @staticmethod
    def update_status(wishlist_id, new_status):
        """
        快速更新願望清單狀態
        :param wishlist_id: 願望清單 ID
        :param new_status: 新狀態 ('pending', 'matched', 'completed', 'cancelled')
        :return: bool 是否成功
        """
        return Wishlist.update(wishlist_id, {'status': new_status})

    @staticmethod
    def delete(wishlist_id):
        """
        刪除願望清單記錄
        :param wishlist_id: 願望清單 ID
        :return: bool 是否成功
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM wishlists WHERE id = ?', (wishlist_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error in Wishlist.delete: {e}")
            return False
