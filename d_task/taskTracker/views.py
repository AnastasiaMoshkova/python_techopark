from django.shortcuts import render
from .models import Tasks
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
import os
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def add(request):

    if request.method == 'POST':
        datas=request.body
        s=datas.decode('utf-8')
        data = json.loads(s)
        name = data.get('name')
        key = data.get('key')
        user_id = data.get('user_id')
        parent_id = data.get('parent_id')
        task=Tasks(name=name, key= key,user_id=user_id,parent_id=parent_id,status = 'ADD')
        task.save()

        return HttpResponse('create success')
    else:
        return HttpResponse('bad request', status=400)


def task(request):
    tasks_tr = Tasks.objects.all()

    users_tr = get_user_model().objects.all()

    return render(request, 'taskTracker/task.html', {'tasks': tasks_tr,'users':users_tr })


def status(request,id):

    tasks = Tasks.objects.filter(id=id)
    for task in tasks:
        task.status="FIN"
        task.save()


    return render(request, 'taskTracker/task.html', {'file': key})

def get_task(request,key,user):
    tasks = Tasks.objects.filter(key=key)

    user_name = get_user_model().objects.get(username=user)
    for task in tasks:
        task.user_id =user_name
        task.status = "GET"
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
    if userid:
        users_tr = get_user_model().objects.filter(username=userid)
    else:
        users_tr =[]
    child_tr=Tasks.objects.filter(parent_id=id)
    return render(request, 'taskTracker/task_list.html', {'tasks': tasks_tr,'users':users_tr, 'childrens':child_tr})

