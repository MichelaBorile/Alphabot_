import sqlite3 as sql

def main():
    conn = sql.connect("users.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER AUTO_INCREMENT, 
                                                     email VARCHAR(30) NOT NULL, 
                                                     password VARCHAR(30) NOT NULL,
                                                     PRIMARY KEY (id)
                                                    );""")
    # cur.execute("""INSERT INTO users (email, password) VALUES ('admin@test.it', 'admin')""")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()