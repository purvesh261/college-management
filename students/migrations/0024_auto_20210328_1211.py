# Generated by Django 3.1.4 on 2021-03-28 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0023_attendance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(choices=[('P', 'Present'), ('A', 'Absent')], max_length=10, verbose_name='Status'),
        ),
    ]