from django.db import models

class Distrito(models.Model):
    nombre = models.TextField()
    def __str__(self):
        return self.nombre

class Museo(models.Model):
    ID_ENTIDAD = models.TextField()
    NOMBRE = models.TextField()
    DESCRIPCION_ENTIDAD = models.TextField()
    HORARIO = models.TextField()
    TRANSPORTE = models.TextField()
    ACCESIBILIDAD = models.TextField()
    CONTENT_URL = models.TextField()
    NOMBRE_VIA = models.TextField()
    CLASE_VIAL = models.TextField()
    TIPO_NUM = models.TextField()
    NUM = models.TextField()
    LOCALIDAD = models.TextField()
    PROVINCIA = models.TextField()
    CODIGO_POSTAL = models.TextField()
    BARRIO = models.TextField()
    DISTRITO = models.ForeignKey(Distrito)
    COORDENADA_X = models.TextField()
    COORDENADA_Y = models.TextField()
    LATITUD = models.TextField()
    LONGITUD = models.TextField()
    TELEFONO = models.TextField()
    FAX = models.TextField()
    EMAIL = models.TextField()
    TIPO = models.TextField()
    def __str__(self):
        return self.NOMBRE

class Comentario(models.Model):
    museo = models.ForeignKey(Museo)
    texto = models.TextField()
    usuario = models.TextField()
    fecha = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.texto

class Titulo(models.Model):
    usuario = models.TextField()
    titulo = models.TextField()

class Letra(models.Model):
    usuario = models.TextField()
    letra = models.TextField()

class Color(models.Model):
    usuario = models.TextField()
    color = models.TextField()

class Favorito(models.Model):
    museo = models.ForeignKey(Museo)
    usuario = models.TextField()
    fecha = models.DateTimeField(auto_now = True)

class Like(models.Model):
    museo = models.ForeignKey(Museo)
    usuario = models.TextField()
