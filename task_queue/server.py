import socket
import uuid
import re
from datetime import datetime
from datetime import timedelta
import json
import pandas as pd
import os

FILE = "file.json"

def parser_file(FILE):
    if os.stat(FILE).st_size != 0:
        data = json.load(open(FILE))
        Q = data
    else:
        Q={}
    return Q

def _add(_queue_,_length_,_data_,conn,Q):
    id = uuid.uuid4()
    id = str(uuid.uuid4())
    conn.send(id.encode('utf-8'))
    if _queue_ not in Q:
        Q[_queue_] = []
        Q[_queue_].append({"id":id,"length":_length_,"data":_data_,"time":"","do":False})
    else:
        Q[_queue_].append({"id": id, "length": _length_, "data": _data_, "time": "","do":False})
    return Q

def _get(_queue_,conn,Q):
    counter_do = 0
    if (len(Q[_queue_]) == 0):
        conn.send(b"NONE")
    else:
        for task in Q[_queue_]:
            if task["do"] == False:
                task["do"] = True
                task["time"] = str(datetime.today())
                conn.send(
                    task["id"].encode('utf-8') + b" " + task["length"].encode('utf-8') + b" " + task["data"].encode(
                        'utf-8'))
                break
            else:
                if ((pd.to_datetime(task["time"]).to_pydatetime() - datetime.today()) >= timedelta(minutes=5)):
                    task["time"] = str(datetime.today())
                    conn.send(
                        task["id"].encode('utf-8') + b" " + task["length"].encode('utf-8') + b" " + task["data"].encode(
                            'utf-8'))
                    break
                else:
                    counter_do=counter_do+1
                    if counter_do==len(Q[_queue_]):
                        conn.send(b"NONE")
                        break
    return Q

def _ack(_queue_,_id_,conn,Q):

    if Q[_queue_]:
        for i in range(len(Q[_queue_])):
            if (Q[_queue_][i]["id"] == _id_) and (Q[_queue_][i]["do"] == True):
                if ((pd.to_datetime(Q[_queue_][i]["time"]).to_pydatetime() - datetime.today()) >= timedelta(minutes=5)):
                    Q[_queue_][i]["time"] = ""
                    Q[_queue_][i]["do"] = False
                    break
                else:
                    Q[_queue_].pop(i)
                    conn.send(b"OK")
                    break
    return Q

def _in(_queue_,_id_,conn,Q):
    counter_present=0
    if Q[_queue_]:
        for task in Q[_queue_]:
            if task['id'] == _id_:
                conn.send(b"YES")
                break
            else:
                counter_present = counter_present+1
                if (counter_present==len(Q[_queue_])):
                    conn.send(b"NO")
    else:
        conn.send(b"NO")
    #return Q

def run(conn,Q):
    data = conn.recv(1000000)
    data=data.decode("utf-8")
    data_str = re.split('\s', data)

    with open('file.json', 'w') as outfile:
        if data_str[0] == "ADD":
            queue = _add(data_str[1], data_str[2], data_str[3], conn,Q)
            json.dump(queue, outfile)
        if data_str[0] == "GET":
            queue = _get(data_str[1], conn,Q)
            json.dump(queue, outfile)
        if data_str[0] == "ACK":
            queue = _ack(data_str[1], data_str[2], conn,Q)
            json.dump(queue, outfile)
    if data_str[0] == "IN":
        _in(data_str[1], data_str[2], conn,Q)
    return queue

if __name__ == '__main__':
    queue=parser_file(FILE)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 5555))
    sock.listen(1)
    while True:
        try:
            conn, addr = sock.accept()
            queue=run(conn,queue)
            conn.close()
        except KeyboardInterrupt:
            break


