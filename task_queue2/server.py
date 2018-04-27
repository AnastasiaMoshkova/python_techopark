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
            task_list.append(task.write)
    with open(FILE, 'w') as outfile:
        json.dump(task_list, outfile)


def parser_file(FILE):
    if os.stat(FILE).st_size != 0:
        data = json.load(open(FILE))
        Q_list = data
        for task in Q_list:
            if task[0] not in Q:
                Q[task[0]]=[]
            Q[task[0]].append(Task(task[0],task[1],task[2],task[3],task[4],task[5]))

class Task():
    def __init__(self,_queue_,_length_,_data_,time="",get=False,id=0):
        self._queue = _queue_
        self._length = _length_
        self._data = _data_
        self._get = get
        self._time = time
        self._id = id
        self._next_task = False

    @property
    def write(self):
        return [self._queue,self._length,self._data,self._get,self._time,self._id]

    @property
    def add(self):
        self._id=str(uuid.uuid4())
        return self._id.encode('utf-8')

    @property
    def get(self,):
        if not self._get:
            self.timeStart
            return self.getSend
        else:
            if self.checkTime:
                self.timeStart
                return self.getSend
            else:
                self._next_task=False
        return self._next_task

    @property
    def getSend(self):
        return self._id.encode('utf-8') + b" " + self._length.encode('utf-8') + b" " + self._data.encode('utf-8')

    @property
    def ack(self):
        if self._get:
            if not self.checkTime:
                return b"OK"

    @property
    def timeStart(self):
        self._time=str(datetime.now())
        self._get = True

    @property
    def checkTime(self):
        return (datetime.strptime(self._time, '%Y-%m-%d %H:%M:%S.%f') - datetime.now()) >= timedelta(minutes=5)

    @property
    def id(self):
        return self._id


def run(conn):
    data = conn.recv(1000000)
    data=data.decode("utf-8")
    data_str = re.split('\s', data)
    name_que = data_str[1]

    if data_str[0] == "ADD":
        task = Task(data_str[1], data_str[2], data_str[3])
        conn.send(task.add)
        if name_que not in Q:
            Q[name_que] = []
        Q[name_que].append(task)
        write_file(Q)

    if data_str[0] == "GET":
        if (len(Q[name_que]) == 0) or not Q[name_que]:
            conn.send(b"NONE")
        else:
            for i in range(len(Q[name_que])):
                result = Q[name_que][i].get
                if result:
                    conn.send(result)
                    break
                else:
                    if (i == len(Q[name_que])):
                        conn.send(b"NONE")
                        continue
        write_file(Q)


    if data_str[0] == "ACK":
        if len(Q[name_que]) != 0:
            for i in range(len(Q[name_que])):
                if (Q[name_que][i].id == data_str[2]):
                    answer = Q[name_que][i].ack
                    Q[name_que].pop(i)
                    conn.send(answer)
                    break
        write_file(Q)

    if data_str[0] == "IN":
        if (len(Q[name_que])==0) or not Q[name_que]:
            conn.send(b"NO")
        else:
            for i in range(len(Q[name_que])):
                if (Q[name_que][i].id == data_str[2]):
                    conn.send(b"YES")
                    break
                if (i==len(Q[name_que])-1) and (Q[name_que][i].id != data_str[2]):
                    conn.send(b"NO")
                    break



if __name__ == '__main__':
    if os.path.isfile(FILE):
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
            conn.close()
            break