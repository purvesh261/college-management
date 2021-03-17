# Generated by Django 3.1.4 on 2021-03-16 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0026_auto_20210314_1331'),
        ('common', '0012_merge_20210304_0926'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('assignment_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('start_date', models.DateField(blank=True, verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, verbose_name='End Date')),
                ('title', models.CharField(max_length=160, verbose_name='Title')),
                ('description', models.TextField(blank=True, default='', max_length=300, verbose_name='Description')),
                ('assignment_file', models.FileField(blank=True, upload_to='assignments', verbose_name='Assignment File')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.course')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.staff')),
            ],
        ),
    ]
