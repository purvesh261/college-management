# Generated by Django 3.1.4 on 2021-04-07 04:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0029_doubts'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Doubts',
            new_name='Doubt',
        ),
    ]