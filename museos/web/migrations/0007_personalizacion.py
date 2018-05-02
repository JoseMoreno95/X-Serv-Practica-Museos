# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_favorito_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='Personalizacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('usuario', models.TextField()),
                ('titulo', models.TextField()),
                ('letra', models.TextField()),
                ('color', models.TextField()),
            ],
        ),
    ]
