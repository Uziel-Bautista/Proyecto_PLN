from django.db import models
import re
import string
from collections import Counter
import nltk
from django.core.exceptions import ValidationError

class TextoAnalizado(models.Model):
    titulo = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='textos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    n_grama = models.IntegerField(default=1, help_text="Tamaño del n-grama (1 = palabras, 2 = bigramas, 3 = trigramas, etc.)")

    def __str__(self):
        return self.titulo

    def clean(self):
        if self.archivo:
            if not self.archivo.name.endswith('.txt'):
                raise ValidationError('Solo se permiten archivos de texto (.txt)')
        if self.n_grama < 1:
            raise ValidationError('El tamaño del n-grama debe ser mayor o igual a 1.')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.procesar_texto()

    def procesar_texto(self):
        from .models import Palabra
        self.palabras.all().delete()

        try:
            with open(self.archivo.path, 'r', encoding='utf-8') as f:
                contenido = f.read().lower()
        except UnicodeDecodeError:
            with open(self.archivo.path, 'r', encoding='latin-1') as f:
                contenido = f.read().lower()

        contenido = contenido.translate(str.maketrans('', '', string.punctuation + '¿¡'))

        try:
            stop_words = set(nltk.corpus.stopwords.words('spanish'))
        except LookupError:
            nltk.download('stopwords')
            stop_words = set(nltk.corpus.stopwords.words('spanish'))

        palabras = re.findall(r'\b\w+\b', contenido)
        palabras_filtradas = [p for p in palabras if p not in stop_words and len(p) > 2]

        if self.n_grama > 1:
            ngramas = zip(*[palabras_filtradas[i:] for i in range(self.n_grama)])
            palabras_filtradas = [' '.join(ng) for ng in ngramas]

        frecuencias = Counter(palabras_filtradas)

        for palabra, frecuencia in frecuencias.most_common(50):
            Palabra.objects.create(texto=self, contenido=palabra, frecuencia=frecuencia)


class Palabra(models.Model):
    texto = models.ForeignKey(TextoAnalizado, on_delete=models.CASCADE, related_name='palabras')
    contenido = models.CharField(max_length=200)
    frecuencia = models.IntegerField()

    class Meta:
        ordering = ['-frecuencia']

    def __str__(self):
        return f"{self.contenido}: {self.frecuencia}"
