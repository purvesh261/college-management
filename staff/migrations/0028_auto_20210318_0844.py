# Generated by Django 3.1.4 on 2021-03-18 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0027_auto_20210317_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='branch',
            field=models.CharField(choices=[('01', 'Computer Engineering'), ('02', 'Information Technology')], max_length=70, verbose_name='Branch'),
        ),
    ]
