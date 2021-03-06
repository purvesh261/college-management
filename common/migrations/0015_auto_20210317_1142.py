# Generated by Django 3.1.4 on 2021-03-17 06:12

import common.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0014_auto_20210317_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='assignment_file',
            field=models.FileField(blank=True, upload_to='assignments', validators=[common.validators.validate_file_extension], verbose_name='Assignment File'),
        ),
    ]
