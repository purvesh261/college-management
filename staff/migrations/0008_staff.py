# Generated by Django 3.1.4 on 2021-01-03 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('staff', '0007_delete_staff'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(default='', max_length=70, verbose_name='First Name')),
                ('middleName', models.CharField(blank=True, default='', max_length=70, verbose_name='Middle Name')),
                ('lastName', models.CharField(default='', max_length=70, verbose_name='Last Name')),
                ('username', models.CharField(max_length=70, verbose_name='Username')),
                ('passwd', models.CharField(max_length=70, verbose_name='Password')),
                ('date', models.DateField(max_length=70, verbose_name='Date of Birth')),
                ('mobile', models.CharField(max_length=10, verbose_name='Mobile Number')),
                ('branch', models.CharField(choices=[('CE', 'Computer Engineering'), ('IT', 'Information Technology'), ('EC', 'Electronics and Comm. Engineering'), ('BME', 'Bio-Medical Engineering'), ('MC', 'Mechantronics Engineering'), ('ME', 'Mechanical Engineering'), ('CE', 'Civil Engineering'), ('EE', 'Electrical Engineering'), ('ME', 'Marine Engineering'), ('AE', 'Automobile Engineering'), ('PE', 'Petrochemical Engineering')], max_length=70, verbose_name='Branch')),
                ('email', models.EmailField(max_length=70, verbose_name='Email')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=7, verbose_name='Gender')),
                ('designation', models.CharField(choices=[('HOD', 'Head of Department'), ('PROF', 'Professor'), ('APROF', 'Assistant Professor'), ('LI', 'Lab Instructor'), ('LA', 'Lab Assistant')], default='', max_length=20, verbose_name='Designation')),
                ('isAdmin', models.BooleanField(default=False, max_length=10)),
            ],
        ),
    ]