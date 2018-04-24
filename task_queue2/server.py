import socket
import uuid
import re
from datetime import datetime
from datetime import timedelta
import json
import os
Q={}
FILE = "file.json"
def write_file(Q):
    task_list=[]
    Q_list=Q.values()
    for list_task in Q_list:
        for task in list_task:
            task_list.append(task.write())
    return task_list

def parser_file(FILE):
    if os.stat(FILE).st_size != 0:
        data = json.load(open(FILE))
        Q_list = data
        for task in Q_list:
            if task[0] not in Q:
                Q[task[0]]=[]
            Q[task[0]].append(Task(task[0],task[1],task[2],task[3],task[4],task[5]))

class Task():
    def __init__(self,_queue_,_length_,_data_,time="",get=False,id=str(uuid.uuid4())):
        self._queue = _queue_
        self._length = _length_
        self._data = _data_
        self._get = get
        self._time = time
        self._id = id
        self._next_task = False

    def write(self):
        return [self._queue,self._length,self._data,self._get,self._time,self._id]

    def add(self,conn):
        conn.send(self._id.encode('utf-8'))

    def get(self,conn):
        if not self._get:
            self.timeStart()
            self.getSend(conn)
        else:
            if self.checkTime():
                self.timeStart()
                self.getSend(conn)
            else:
                self._next_task=True
        return self._next_task

    def getSend(self,conn):
        conn.send(self._id.encode('utf-8') + b" " + self._length.encode('utf-8') + b" " + self._data.encode('utf-8'))

    def ack(self,conn):
        if self._get:
            if not self.checkTime():
                conn.send(b"OK")

    def timeStart(self):
        self._time=str(datetime.now())
        self._get = True

    def checkTime(self):
        return (datetime.strptime(self._time, '%Y-%m-%d %H:%M:%S.%f') - datetime.now()) >= timedelta(minutes=5)

    def id(self):
        return self._id

    def status(self):
        return self._get



def run(conn):
    data = conn.recv(1000000)
    data=data.decode("utf-8")
    data_str = re.split('\s', data)
    name_que = data_str[1]
    with open(FILE, 'w') as outfile:
        if data_str[0] == "ADD":
            task = Task(data_str[1], data_str[2], data_str[3])
            task.add(conn)
            if name_que not in Q:
                Q[name_que] = []
            Q[name_que].append(task)
            json.dump(write_file(Q), outfile)

        if data_str[0] == "GET":
            if len(Q[name_que]) == 0:
                conn.send(b"NONE")
            else:
                for i in range(len(Q[name_que])):
                    if Q[name_que][i].get(conn):
                        if (i == len(Q[name_que])):
                            conn.send(b"NONE")
                        continue
                    else:
                        break
            json.dump(write_file(Q), outfile)

        if data_str[0] == "ACK":
            if len(Q[name_que])!=0:
                for i in range(len(Q[name_que])):
                    if (Q[name_que][i].id() == data_str[2]):
                        Q[name_que][i].ack(conn)
                        Q[name_que].pop(i)
                        break
            json.dump(write_file(Q), outfile)

    if data_str[0] == "IN":
        if len(Q[name_que])==0:
            conn.send(b"NO")
        else:
            for i in range(len(Q[name_que])):
                if (Q[name_que][i].id() == data_str[2]):
                    conn.send(b"YES")
                    break
                if (i==len(Q[name_que])) and (Q[name_que][i].id() != data_str[2]):
                    conn.send(b"NO")
                    break



if __name__ == '__main__':
    parser_file(FILE)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 5555))
    sock.listen(1)
    while True:
        try:
            conn, addr = sock.accept()
            queue=run(conn)
            conn.close()
        except KeyboardInterrupt:
            break