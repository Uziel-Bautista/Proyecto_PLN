from django.db import models
import re
from collections import Counter

class TextoAnalizado(models.Model):
    titulo = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='textos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    def procesar_texto(self):
        from .models import Palabra
        self.palabras.all().delete()  # Limpiar palabras previas si re-procesamos
        
        
        with open(self.archivo.path, 'r', encoding='utf-8') as f:
            contenido = f.read().lower()
        
        # Mejor procesamiento con regex para capturar mejor las palabras
        palabras = re.findall(r'\b\w+\b', contenido)
        frecuencias = {}
        for palabra in palabras:
            frecuencias[palabra] = frecuencias.get(palabra, 0) + 1
        
        for palabra, frecuencia in frecuencias.items():
            Palabra.objects.create(texto=self, contenido=palabra, frecuencia=frecuencia)

class Palabra(models.Model):
    texto = models.ForeignKey(TextoAnalizado, on_delete=models.CASCADE, related_name='palabras')
    contenido = models.CharField(max_length=100)
    frecuencia = models.IntegerField()

    def __str__(self):
        return f"{self.contenido}: {self.frecuencia}"
