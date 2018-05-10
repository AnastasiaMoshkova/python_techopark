import sqlite3


conn = sqlite3.connect('mydb.db')
c = conn.cursor()

c.execute('''PRAGMA foreign_keys = ON''')
c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY,first_name TEXT,last_name TEXT,login TEXT)''')
c.execute('''CREATE TABLE tasks (id INTEGER PRIMARY KEY,name TEXT,status TEXT,parent_id INTEGER,user_id INTEGER,
FOREIGN KEY (parent_id) REFERENCES tasks(id),
FOREIGN KEY (user_id) REFERENCES users(id))''')


c.execute("INSERT INTO users (first_name,last_name,login) VALUES ('Ivan','Ivanov','IIvanov')")
conn.commit()
c.execute("INSERT INTO users (first_name,last_name,login) VALUES ('Petr','Petrov','PPetrov')")
conn.commit()
c.execute("INSERT INTO users (first_name,last_name,login) VALUES ('Michail','Alekseev','MAlekseev')")
conn.commit()

c.execute('SELECT * FROM users')
row = c.fetchone()
# выводим список пользователей в цикле
while row is not None:
    print("id:" + str(row[0]) + " имя: " + row[1] + " | фамилия: " + row[2] + "| login: " + row[3])
    row = c.fetchone()
c.close()
conn.close()

