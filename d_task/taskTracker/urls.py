from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.task, name='task'),
    #url(r'^add/(?P<anystring>\d+)/(?P<anystring>.+)/$', views.add),
    #url(r'^add/(?P<anystring>\d+)/(?P<anystring>.+)/page(?P<anystring>.+)/$', views.add),
    url(r'^add/(?P<json_file>[\w]+).json$', views.add, name='add'),
    url(r'status/(?P<key>\w+)/$', views.status, name='status'),
    url(r'get/(?P<key>\w+)/(?P<user>\w+)/$', views.get_task, name='get_task'),
    url(r'find/(?P<id>\w+)/$', views.find, name='find'),
    url(r'tasks/(?P<id>\w+)/$', views.user_tasks, name='user_tasks'),
    url(r'list/(?P<id>\w+)/$', views.list_task, name='list_task'),
]