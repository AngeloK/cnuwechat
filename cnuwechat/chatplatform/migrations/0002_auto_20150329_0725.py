# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatplatform', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='teacherID',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='courseID',
        ),
        migrations.DeleteModel(
            name='Course',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='studentID',
        ),
        migrations.DeleteModel(
            name='Schedule',
        ),
        migrations.RemoveField(
            model_name='student',
            name='departmentID',
        ),
        migrations.DeleteModel(
            name='Department',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
        migrations.DeleteModel(
            name='Teacher',
        ),
    ]
