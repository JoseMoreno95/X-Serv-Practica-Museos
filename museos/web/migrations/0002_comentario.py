# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('texto', models.TextField()),
                ('usuario', models.TextField()),
                ('fecha', models.DateField(auto_now=True)),
                ('museo', models.ForeignKey(to='web.Museo')),
            ],
        ),
    ]
