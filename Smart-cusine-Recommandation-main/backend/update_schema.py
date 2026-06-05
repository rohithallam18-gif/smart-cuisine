import sqlite3

def update_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # Try to add password column
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN password TEXT")
        print("Column 'password' added successfully.")
    except sqlite3.OperationalError:
        print("Column 'password' already exists.")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_db()
