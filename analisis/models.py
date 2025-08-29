from django.db import models
import re
import string
from collections import Counter
import nltk
from django.core.exceptions import ValidationError

# Asegúrate de descargar las stopwords si no lo has hecho antes:
# import nltk
# nltk.download('stopwords')

class TextoAnalizado(models.Model):
    titulo = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='textos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    def clean(self):
        # Validar que el archivo sea de texto
        if self.archivo:
            if not self.archivo.name.endswith('.txt'):
                raise ValidationError('Solo se permiten archivos de texto (.txt)')

    def save(self, *args, **kwargs):
        # Primero guardar el objeto
        super().save(*args, **kwargs)
        # Luego procesar el texto
        self.procesar_texto()

    def procesar_texto(self):
        # Importar aquí para evitar circular imports
        from .models import Palabra
        
        # Limpiar palabras previas si re-procesamos
        self.palabras.all().delete()

        try:
            # Leer el contenido y convertir a minúsculas
            with open(self.archivo.path, 'r', encoding='utf-8') as f:
                contenido = f.read().lower()
        except UnicodeDecodeError:
            # Intentar con otra codificación si utf-8 falla
            with open(self.archivo.path, 'r', encoding='latin-1') as f:
                contenido = f.read().lower()

        # Eliminar puntuación
        contenido = contenido.translate(str.maketrans('', '', string.punctuation + '¿¡'))

        # Obtener stopwords en español
        try:
            stop_words = set(nltk.corpus.stopwords.words('spanish'))
        except LookupError:
            # Si no están descargadas las stopwords, usar un conjunto vacío
            nltk.download('stopwords')
            stop_words = set(nltk.corpus.stopwords.words('spanish'))

        # Extraer palabras usando regex
        palabras = re.findall(r'\b\w+\b', contenido)

        # Filtrar stopwords y palabras muy cortas (menos de 2 caracteres)
        palabras_filtradas = [p for p in palabras if p not in stop_words and len(p) > 2]

        # Contar frecuencias
        frecuencias = Counter(palabras_filtradas)

        # Guardar palabras en la base de datos (solo las 50 más frecuentes)
        for palabra, frecuencia in frecuencias.most_common(50):
            Palabra.objects.create(texto=self, contenido=palabra, frecuencia=frecuencia)


class Palabra(models.Model):
    texto = models.ForeignKey(TextoAnalizado, on_delete=models.CASCADE, related_name='palabras')
    contenido = models.CharField(max_length=100)
    frecuencia = models.IntegerField()

    class Meta:
        ordering = ['-frecuencia']

    def __str__(self):
        return f"{self.contenido}: {self.frecuencia}"