# Generated by Django 3.1.4 on 2021-02-10 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0024_merge_20210210_0849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='branch',
            field=models.CharField(choices=[('Computer Engineering', 'Computer Engineering'), ('Information Technology', 'Information Technology')], max_length=70, verbose_name='Branch'),
        ),
    ]
