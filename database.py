import sqlite3

# Bazani yaratish
def create_connection():
    conn = sqlite3.connect('bot_database.db')
    return conn

def create_admin_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY,
        user_id INTEGER UNIQUE NOT NULL,
        telegram_username TEXT
    )
    ''')
    conn.commit()
    conn.close()

def create_file_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        keyword TEXT UNIQUE NOT NULL,
        file_path TEXT NOT NULL,
        admin_id INTEGER NOT NULL,
        FOREIGN KEY (admin_id) REFERENCES admins (id)
    )
    ''')
    conn.commit()
    conn.close()

def save_file(name, keyword, file_path, admin_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('INSERT INTO files (name, keyword, file_path, admin_id) VALUES (?, ?, ?, ?)', (name, keyword, file_path, admin_id))
    conn.commit()
    conn.close()

def get_file_by_keyword(keyword):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT name, file_path FROM files WHERE keyword = ?', (keyword,))
    file_data = c.fetchone()
    conn.close()
    return file_data

def get_file_by_id(file_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM files WHERE id = ?', (file_id,))
    file_data = c.fetchone()
    conn.close()
    return file_data

def add_admin(user_id, telegram_username):
    conn = create_connection()
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO admins (user_id, telegram_username) VALUES (?, ?)', (user_id, telegram_username))
    conn.commit()
    conn.close()

def is_admin(user_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM admins WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    return result is not None

def get_all_files():
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM files')
    files = c.fetchall()
    conn.close()
    return files

def get_all_admins():
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT id, user_id, telegram_username FROM admins')
    admins = c.fetchall()
    conn.close()
    return admins

def delete_file(file_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('DELETE FROM files WHERE id = ?', (file_id,))
    conn.commit()
    conn.close()
    return c.rowcount > 0  # O'chirish muvaffaqiyatli bo'lsa True, aks holda False

def delete_admin(user_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('DELETE FROM admins WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    return c.rowcount > 0  # O'chirish muvaffaqiyatli bo'lsa True, aks holda False