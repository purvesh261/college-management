# Generated by Django 3.1.4 on 2021-03-17 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0013_assignment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='End Date'),
        ),
    ]