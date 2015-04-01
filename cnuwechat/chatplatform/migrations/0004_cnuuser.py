# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatplatform', '0003_auto_20150329_0727'),
    ]

    operations = [
        migrations.CreateModel(
            name='CnuUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('openid', models.CharField(unique=True, max_length=100)),
                ('studentid', models.CharField(unique=True, max_length=100)),
                ('jsessionid', models.CharField(max_length=100)),
                ('iplanetdirectorypro', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
