import sqlite3

class Tasktracker:
    def __init__(self,bd):
        try:
            self._conn = sqlite3.connect(bd)
            self._cursor=self._conn.cursor()
            self._cursor.execute('''PRAGMA foreign_keys = ON''')
        except sqlite3.Error as e:
            print('Ошибка БД: ' + str(e))

    def add(self,name, parent_task=None):
        if parent_task:
            self._cursor.execute("INSERT INTO tasks (name,status,parent_id) VALUES ('%s','%s',(SELECT id FROM tasks WHERE name='%s'))" % (name,"добавлено",parent_task))
            self._conn.commit()
        else:
            self._cursor.execute("INSERT INTO tasks (name,status,parent_id) VALUES ('%s','%s',NULL)" % (name,"добавлено"))
            self._conn.commit()

    def get(self,user_name,name_task):
        self._cursor.execute("UPDATE tasks SET status ='взято',user_id =(SELECT id FROM users WHERE login='%s') WHERE (SELECT id FROM tasks WHERE name='%s')=parent_id OR name='%s'"% (user_name,name_task,name_task))
        self._conn.commit()

    def ack(self,name_task):
        self._cursor.execute(
            "UPDATE tasks SET status ='выполнено' WHERE parent_id =(SELECT id FROM tasks WHERE name='%s') OR name='%s'" % (
            name_task, name_task))
        self._conn.commit()

    def get_status(self,name_task):
        self._cursor.execute("SELECT status FROM tasks WHERE name = '%s'" % (name_task))
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
            print("id:" + str(row[0]) + " name: " + str(row[1]) + " | status: " + str(row[2]) + "| parent_id: " + str(row[3])+ "| user_id: " + str(row[4]))
            row = self._cursor.fetchone()

obj=Tasktracker('mydb.db')

obj.show_users

obj.add("покупки")
obj.add("овощи","покупки")
obj.add("фрукты","покупки")
obj.add("ягоды","покупки")

obj.add("домашнее задание")
obj.add("задача1","домашнее задание")
obj.add("задача2","домашнее задание")
obj.add("задача3","домашнее задание")

obj.add("помыть машину")

obj.add("отправить письмо")

obj.show_tasks

obj.get('MAlekseev',"фрукты")
obj.get('PPetrov',"домашнее задание")
obj.get('IIvanov',"помыть машину")

print(obj.get_status("отправить письмо"))


obj.show_tasks

obj.ack("фрукты")
obj.ack("домашнее задание")

print(obj.get_status("домашнее задание"))

obj.show_tasks

obj.finish






