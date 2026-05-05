-- schema.sql
-- 選課交換平台 SQLite 建表語法

-- 啟用 Foreign Key 支援
PRAGMA foreign_keys = ON;

-- 1. 使用者表 (users)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    credit_score INTEGER DEFAULT 100,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. 課程表 (courses)
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    department TEXT,
    instructor TEXT,
    credits INTEGER DEFAULT 0
);

-- 3. 許願清單表 (wishlists)
CREATE TABLE IF NOT EXISTS wishlists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    held_course_id INTEGER NOT NULL,
    target_course_id INTEGER NOT NULL,
    status TEXT DEFAULT 'pending', -- pending, matched, completed, cancelled
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (held_course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (target_course_id) REFERENCES courses(id) ON DELETE CASCADE
);

-- 4. 配對紀錄表 (matches)
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    wishlist_id_1 INTEGER NOT NULL,
    wishlist_id_2 INTEGER NOT NULL,
    status TEXT DEFAULT 'chatting', -- chatting, completed, cancelled
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (wishlist_id_1) REFERENCES wishlists(id) ON DELETE CASCADE,
    FOREIGN KEY (wishlist_id_2) REFERENCES wishlists(id) ON DELETE CASCADE
);

-- 5. 聊天訊息表 (chat_messages)
CREATE TABLE IF NOT EXISTS chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    sender_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id) REFERENCES matches(id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE
);
