# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_comentario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='museo',
            name='DATOSCONTACTOS',
        ),
        migrations.RemoveField(
            model_name='museo',
            name='LOCALIZACION',
        ),
    ]
