# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Museo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('ID_ENTIDAD', models.TextField()),
                ('NOMBRE', models.TextField()),
                ('DESCRIPCION_ENTIDAD', models.TextField()),
                ('HORARIO', models.TextField()),
                ('TRANSPORTE', models.TextField()),
                ('ACCESIBILIDAD', models.TextField()),
                ('CONTENT_URL', models.TextField()),
                ('LOCALIZACION', models.TextField()),
                ('NOMBRE_VIA', models.TextField()),
                ('CLASE_VIAL', models.TextField()),
                ('TIPO_NUM', models.TextField()),
                ('NUM', models.TextField()),
                ('LOCALIDAD', models.TextField()),
                ('PROVINCIA', models.TextField()),
                ('CODIGO_POSTAL', models.TextField()),
                ('BARRIO', models.TextField()),
                ('DISTRITO', models.TextField()),
                ('COORDENADA_X', models.TextField()),
                ('COORDENADA_Y', models.TextField()),
                ('LATITUD', models.TextField()),
                ('LONGITUD', models.TextField()),
                ('DATOSCONTACTOS', models.TextField()),
                ('TELEFONO', models.TextField()),
                ('FAX', models.TextField()),
                ('EMAIL', models.TextField()),
                ('TIPO', models.TextField()),
            ],
        ),
    ]
