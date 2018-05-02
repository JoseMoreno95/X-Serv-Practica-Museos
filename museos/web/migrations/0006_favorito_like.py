# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20180501_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('usuario', models.TextField()),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('hotel', models.ForeignKey(to='web.Museo')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('usuario', models.TextField()),
                ('hotel', models.ForeignKey(to='web.Museo')),
            ],
        ),
    ]
