# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('courseName', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'course',
                'verbose_name_plural': 'courses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('departmentName', models.CharField(max_length=50)),
                ('departmentURL', models.URLField()),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('week', models.CharField(max_length=50)),
                ('score', models.CharField(max_length=50, null=True)),
                ('courseID', models.ForeignKey(to='chatplatform.Course')),
            ],
            options={
                'verbose_name': 'Schedule',
                'verbose_name_plural': 'Schedules',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stuID', models.CharField(unique=True, max_length=20)),
                ('password', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('card_balance', models.CharField(max_length=100)),
                ('flow_balance', models.CharField(max_length=100)),
                ('departmentID', models.ForeignKey(to='chatplatform.Department')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('profession', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'teacher',
                'verbose_name_plural': 'teachers',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='schedule',
            name='studentID',
            field=models.ForeignKey(to='chatplatform.Student', to_field=b'stuID'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='teacherID',
            field=models.ForeignKey(to='chatplatform.Teacher'),
            preserve_default=True,
        ),
    ]
