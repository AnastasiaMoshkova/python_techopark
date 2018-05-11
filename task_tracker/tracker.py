import sqlite3

class Tasktracker:
    def __init__(self,bd):
        try:
            self._conn = sqlite3.connect(bd)
            self._cursor=self._conn.cursor()
            self._cursor.execute('''PRAGMA foreign_keys = ON''')
        except sqlite3.Error as e:
            print('Ошибка БД: ' + str(e))

    def add(self,name, key,parent_task=None):
        if parent_task:
            self._cursor.execute('''INSERT INTO tasks (name,key,status,parent_id) 
            VALUES ('%s','%s','%s',(SELECT id FROM tasks WHERE name='%s'))''' % (name,key,"добавлено",parent_task))
            self._conn.commit()
        else:
            self._cursor.execute('''INSERT INTO tasks (name,key,status,parent_id) 
            VALUES ('%s','%s','%s',NULL)''' % (name,key,"добавлено"))
            self._conn.commit()


    def get_status(self,id_task):
        self._cursor.execute('''SELECT status FROM tasks WHERE id = '%d' ''' % (id_task))
        row = self._cursor.fetchone()
        self._conn.commit()
        return row[0]

    @property
    def finish(self):
        self._cursor.close()
        self._conn.close()

    @property
    def show_users(self):
        self._cursor.execute('SELECT * FROM users')
        row = self._cursor.fetchone()
        while row is not None:
            print("id:" + str(row[0]) + " имя: " + row[1] + " | фамилия: " + row[2] + "| login: " + row[3])
            row = self._cursor.fetchone()

    @property
    def show_tasks(self):
        self._cursor.execute('SELECT * FROM tasks')
        row = self._cursor.fetchone()
        while row is not None:
            print("id:" + str(row[0]) + " key: " + str(row[1]) + " | name: " + str(row[2]) + "| status: " + str(row[3])+ "| parent_id: " + str(row[4])+ "| user_id: " + str(row[5]))
            row = self._cursor.fetchone()

    @property
    def show_table(self):
        self._cursor.execute('''SELECT k.name, t.name,u.first_name,u.last_name 
        AS data 
        FROM tasks t 
        INNER JOIN users u ON t.user_id=u.id
        INNER JOIN tasks k ON t.parent_id=k.id''')
        row = self._cursor.fetchone()
        while row is not None:
            print("task: " + str(row[0]) + " parent: " + str(row[1]) + " | name: " + str(row[2]) + "| last_name: " + str(row[3]))
            row = self._cursor.fetchone()

    def get(self, login, key_task):
        self._cursor.execute(
            '''WITH recursive tree AS ( 
    SELECT id, parent_id, key FROM tasks
    WHERE parent_id is NULL
    UNION ALL
    SELECT tasks.id, tasks.parent_id, tree.key
    FROM tasks
    JOIN tree ON tasks.parent_id = tree.id
    )
        UPDATE tasks SET status ='взято',user_id =(SELECT id FROM users WHERE login='%s') 
        WHERE id IN (SELECT id FROM tree WHERE key = '%s')
        ''' % (login,key_task))
        self._conn.commit()

    def ack(self, key_task):
        self._cursor.execute(
            '''WITH recursive tree AS ( 
    SELECT id, parent_id, key FROM tasks
    WHERE parent_id is NULL
    UNION ALL
    SELECT tasks.id, tasks.parent_id, tree.key
    FROM tasks
    JOIN tree ON tasks.parent_id = tree.id
    )
        UPDATE tasks SET status ='выполнено' WHERE id IN (SELECT id FROM tree WHERE key = '%s')
        ''' % (key_task))
        self._conn.commit()


obj=Tasktracker('mydb.db')






