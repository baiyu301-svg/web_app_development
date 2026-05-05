import sqlite3
import os

def get_db_connection():
    """建立並回傳資料庫連線，回傳結果為 sqlite3.Row 型別，方便像字典般存取資料"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')
    
    # 確保 instance 目錄存在
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
