import sqlite3


conn = sqlite3.connect('mydb.db')
c = conn.cursor()

c.execute('''PRAGMA foreign_keys = ON''')
c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY,first_name char(20),last_name char(20),login char(40))''')
c.execute('''CREATE TABLE tasks (id INTEGER PRIMARY KEY,name char(20),status TEXT,parent_id INTEGER,user_id INTEGER,
FOREIGN KEY (parent_id) REFERENCES tasks(id),
FOREIGN KEY (user_id) REFERENCES users(id))''')

a = ['vadim', 'vladimir','igor','michael','dmitry','eygeniy','aleksander','ivan']
b = ['pushtaev', 'denisov','ivanov','petrov','sidorov','rudny','sokolov','shilov']
import random
users = []
for i in range(10000):
    users.append((random.choice(a), random.choice(b), '{}{}{}'.format(random.choice(a)[0], random.choice(b), i)))
print(users)
result = []
for user_item in users:
    result.append('("{}", "{}", "{}")'.format(user_item[0], user_item[1], user_item[2]))

c.execute("INSERT INTO users (first_name,last_name,login) VALUES" + ', '.join(result))
conn.commit()

task=[]
for i in range(90000):
    task.append('("{}", "{}",{},{})'.format('task'+str(i), "добавлено", 'NULL', 'NULL'))

for i in range(10000):
    task.append('("{}", "{}",{},{})'.format('task_user'+str(i), "добавлено", 'NULL', random.randint(1,10000)))

c.execute("INSERT INTO tasks (name,status,parent_id,user_id) VALUES"+', '.join(task))
conn.commit()
c.close()
conn.close()