# Generated by Django 4.0.2 on 2022-02-22 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0003_alter_todo_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='description',
        ),
    ]
