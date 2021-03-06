# Generated by Django 3.1.4 on 2021-01-02 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_auto_20210102_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='branch',
            field=models.CharField(choices=[('CE', 'Computer Engineering'), ('IT', 'Information Technology'), ('EC', 'Electronics and Comm. Engineering'), ('BME', 'Bio-Medical Engineering'), ('MC', 'Mechantronics Engineering'), ('ME', 'Mechanical Engineering'), ('CE', 'Civil Engineering'), ('EE', 'Electrical Engineering'), ('ME', 'Marine Engineering'), ('AE', 'Automobile Engineering'), ('PE', 'Petrochemical Engineering')], max_length=70, verbose_name='Branch'),
        ),
        migrations.AlterField(
            model_name='student',
            name='date',
            field=models.DateField(max_length=70, verbose_name='Date of Birth'),
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(max_length=70, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='student',
            name='enrolment',
            field=models.CharField(max_length=70, primary_key=True, serialize=False, verbose_name='Enrolment Number'),
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=7, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='student',
            name='mobile',
            field=models.CharField(max_length=10, verbose_name='Mobile Number'),
        ),
        migrations.AlterField(
            model_name='student',
            name='sem',
            field=models.CharField(choices=[('1', 'I'), ('2', 'II'), ('3', 'III'), ('4', 'IV'), ('5', 'V'), ('6', 'VI'), ('7', 'VII'), ('8', 'VIII')], max_length=5, verbose_name='Semester'),
        ),
    ]
