from django.contrib import admin
from .models import Museo, Comentario, Distrito, Titulo, Color, Letra, Favorito, Like

# Register your models here.

class DistritoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Distrito, DistritoAdmin)

class MuseoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Museo, MuseoAdmin)

class ComentarioAdmin(admin.ModelAdmin):
    pass
admin.site.register(Comentario, ComentarioAdmin)

class TituloAdmin(admin.ModelAdmin):
    pass
admin.site.register(Titulo, TituloAdmin)

class ColorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Color, ColorAdmin)

class LetraAdmin(admin.ModelAdmin):
    pass
admin.site.register(Letra, LetraAdmin)

class FavoritoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Favorito, FavoritoAdmin)

class LikeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Like, LikeAdmin)
