# Generated by Django 3.1.4 on 2021-01-03 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20210103_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='category',
            field=models.CharField(choices=[('Student', 'Student'), ('Faculty', 'Faculty'), ('Staff', 'Staff'), ('Admin', 'Admin'), ('Head of Department', 'Head of Department')], max_length=70, verbose_name='User Category'),
        ),
    ]
