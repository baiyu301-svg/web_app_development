from app.models import get_db_connection

class Match:
    @staticmethod
    def create(wishlist_id_1, wishlist_id_2):
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

    @staticmethod
    def get_by_id(match_id):
        conn = get_db_connection()
        match = conn.execute('SELECT * FROM matches WHERE id = ?', (match_id,)).fetchone()
        conn.close()
        return dict(match) if match else None

    @staticmethod
    def get_user_matches(user_id):
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

    @staticmethod
    def update_status(match_id, new_status):
        conn = get_db_connection()
        conn.execute('UPDATE matches SET status = ? WHERE id = ?', (new_status, match_id))
        conn.commit()
        conn.close()
