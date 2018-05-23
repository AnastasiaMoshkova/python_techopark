# Generated by Django 2.0.5 on 2018-05-22 21:02

from django.db import migrations
import uuid


def combine_names(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    #Person = apps.get_model("taskTracker", "Person")
    #for person in Person.objects.all():
     #   person.name = "%s %s" % (person.first_name, person.last_name)
      #  person.save()

    Task = apps.get_model("taskTracker", "Tasks")
    db_alias=schema_editor.connection.alias
    Task_list=[]
    for i in range(5):
        Task_list.append(Task(key=str(uuid.uuid4), name='task'+str(i), status='add', parent_id=None, user_id=None))

    Task.objects.using(db_alias).bulk_create(Task_list)

class Migration(migrations.Migration):

    dependencies = [
        ('taskTracker', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(combine_names),
    ]