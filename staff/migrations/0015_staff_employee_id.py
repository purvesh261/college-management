# Generated by Django 3.1.4 on 2021-01-24 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0014_staff_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='employee_id',
            field=models.CharField(default='', max_length=70, unique=True, verbose_name='Employee Id'),
            preserve_default=False,
        ),
    ]