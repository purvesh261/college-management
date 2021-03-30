# Generated by Django 3.1.4 on 2021-03-18 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0021_auto_20210318_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='branch',
            field=models.CharField(choices=[('01', 'Computer Engineering'), ('02', 'Information Technology'), ('03', 'Electronics and Comm. Engineering'), ('04', 'Bio-Medical Engineering'), ('05', 'Mechantronics Engineering'), ('06', 'Mechanical Engineering'), ('07', 'Civil Engineering'), ('08', 'Electrical Engineering'), ('09', 'Marine Engineering'), ('10', 'Automobile Engineering'), ('11', 'Petrochemical Engineering'), ('12', 'Branch of engineering')], max_length=70, verbose_name='Branch'),
        ),
        migrations.AlterField(
            model_name='student',
            name='branch',
            field=models.CharField(choices=[('01', 'Computer Engineering'), ('02', 'Information Technology'), ('03', 'Electronics and Comm. Engineering'), ('04', 'Bio-Medical Engineering'), ('05', 'Mechantronics Engineering'), ('06', 'Mechanical Engineering'), ('07', 'Civil Engineering'), ('08', 'Electrical Engineering'), ('09', 'Marine Engineering'), ('10', 'Automobile Engineering'), ('11', 'Petrochemical Engineering'), ('12', 'Branch of engineering')], max_length=70, verbose_name='Branch'),
        ),
    ]
