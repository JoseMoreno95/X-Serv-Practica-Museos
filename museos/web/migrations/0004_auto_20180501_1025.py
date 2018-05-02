# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20180429_0032'),
    ]

    operations = [
        migrations.CreateModel(
            name='Distrito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='museo',
            name='DISTRITO',
            field=models.ForeignKey(to='web.Distrito'),
        ),
    ]
