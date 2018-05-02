# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_auto_20180502_1403'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('usuario', models.TextField()),
                ('color', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Letra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('usuario', models.TextField()),
                ('letra', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Titulo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('usuario', models.TextField()),
                ('titulo', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='Personalizacion',
        ),
    ]
