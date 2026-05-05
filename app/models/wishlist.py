from app.models import get_db_connection

class Wishlist:
    @staticmethod
    def create(user_id, held_course_id, target_course_id):
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

    @staticmethod
    def get_by_id(wishlist_id):
        conn = get_db_connection()
        wishlist = conn.execute('SELECT * FROM wishlists WHERE id = ?', (wishlist_id,)).fetchone()
        conn.close()
        return dict(wishlist) if wishlist else None

    @staticmethod
    def get_by_user(user_id):
        conn = get_db_connection()
        wishlists = conn.execute('SELECT * FROM wishlists WHERE user_id = ?', (user_id,)).fetchall()
        conn.close()
        return [dict(w) for w in wishlists]

    @staticmethod
    def update_status(wishlist_id, new_status):
        conn = get_db_connection()
        conn.execute('UPDATE wishlists SET status = ? WHERE id = ?', (new_status, wishlist_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(wishlist_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM wishlists WHERE id = ?', (wishlist_id,))
        conn.commit()
        conn.close()
