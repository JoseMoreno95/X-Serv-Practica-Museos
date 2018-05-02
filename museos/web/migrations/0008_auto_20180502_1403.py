# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_personalizacion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favorito',
            old_name='hotel',
            new_name='museo',
        ),
        migrations.RenameField(
            model_name='like',
            old_name='hotel',
            new_name='museo',
        ),
    ]
