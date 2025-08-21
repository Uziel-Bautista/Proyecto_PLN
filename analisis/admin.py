from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import TextoAnalizado, Palabra

@admin.register(TextoAnalizado)
class TextoAnalizadoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_subida')

@admin.register(Palabra)
class PalabraAdmin(admin.ModelAdmin):
    list_display = ('contenido', 'frecuencia', 'texto')
    list_filter = ('texto',)
