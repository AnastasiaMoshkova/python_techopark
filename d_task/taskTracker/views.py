from django.shortcuts import render
from .models import Tasks
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
import os
import json

def task(request):
    tasks_tr = Tasks.objects.all()

    users_tr = get_user_model().objects.all()

    return render(request, 'taskTracker/task.html', {'tasks': tasks_tr,'users':users_tr })


def add(request, json_file):

    directory="C:\\Users\\Nastya\\Pictures\\techno_python"

    with open(os.path.join(directory, json_file +'.json'), 'r', encoding='utf-8') as fh:  # открываем файл на чтение
        json_content = json.load(fh)  # загружаем из файла данные в словарь data

    task = Tasks.objects.create()
    task.name=json_content['name']
    task.key=json_content['key']
    task.parent_id = json_content['parent_id']
    task.status='add'
    task.save()

    return render(request, 'taskTracker/task.html', {'file': json_content['name']})



def status(request,key):

    tasks = Tasks.objects.filter(key=key)
    for task in tasks:
        task.status="finished"
        task.save()


    return render(request, 'taskTracker/task.html', {'file': key})

def get_task(request,key,user):
    tasks = Tasks.objects.filter(key=key)

    user_name = get_user_model().objects.get(username=user)
    for task in tasks:
        #task.user_id = user_name[0].username
        task.user_id =user_name
        task.status = "get"
        task.save()
    return render(request, 'taskTracker/task.html', {'file': user})

def find(request,id):
    tasks = Tasks.objects.filter(id=id)
    return render(request, 'taskTracker/task.html', {'tasks': tasks})

def user_tasks(request,id):
    tasks = Tasks.objects.filter(user_id=id)
    return render(request, 'taskTracker/task.html', {'tasks': tasks})

def list_task(request,id):
    tasks_tr = Tasks.objects.filter(id=id)
    userid=tasks_tr[0].user_id
    taskname = tasks_tr[0].name
    if userid:
        users_tr = get_user_model().objects.filter(username=userid)
    else:
        users_tr =[]
    child_tr=Tasks.objects.filter(parent_id=id)
    return render(request, 'taskTracker/task_list.html', {'tasks': tasks_tr,'users':users_tr, 'childrens':child_tr})
