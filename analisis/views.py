from django.shortcuts import render, redirect, get_object_or_404
from .forms import TextoAnalizadoForm
from .models import TextoAnalizado, Palabra
import nltk
import ssl
import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .utils_ngram_mle import calcular_probabilidades



# Inicialización de NLTK
def initialize_nltk():
    """Inicializa y descarga los recursos necesarios de NLTK"""
    try:
        # Configurar SSL para evitar problemas de certificado
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        
        # Establecer la ruta para datos de NLTK
        nltk_data_dir = os.path.join(settings.BASE_DIR, 'nltk_data')
        if not os.path.exists(nltk_data_dir):
            os.makedirs(nltk_data_dir)
        
        nltk.data.path.append(nltk_data_dir)
        
        # Descargar recursos necesarios
        resources = ['punkt', 'punkt_tab', 'stopwords']
        for resource in resources:
            try:
                if resource == 'stopwords':
                    nltk.data.find(f'corpora/{resource}')
                else:
                    nltk.data.find(f'tokenizers/{resource}')
            except LookupError:
                print(f"Descargando recurso NLTK: {resource}")
                nltk.download(resource, download_dir=nltk_data_dir)
                
    except Exception as e:
        print(f"Error inicializando NLTK: {e}")

# Inicializar NLTK al importar el módulo
initialize_nltk()

# Vista para listar los textos subidos
def lista_textos(request):
    textos = TextoAnalizado.objects.all().order_by('-fecha_subida')
    return render(request, 'analisis/lista.html', {'textos': textos})

# Vista para subir un texto y procesarlo
def subir_texto(request):
    if request.method == 'POST':
        form = TextoAnalizadoForm(request.POST, request.FILES)
        if form.is_valid():
            texto = form.save(commit=False)
            texto.titulo = texto.archivo.name  # Asignar nombre del archivo como título
            texto.save()

            # El procesamiento se hace automáticamente en el modelo con save()
            print(f"Texto guardado: {texto.titulo}")
            print(f"Palabras procesadas: {texto.palabras.count()}")
            
            return redirect('lista_textos')
    else:
        form = TextoAnalizadoForm()
    return render(request, 'analisis/subir.html', {'form': form})

# Vista para ver histograma
def ver_histograma(request, texto_id):
    texto = get_object_or_404(TextoAnalizado, pk=texto_id)
    
    # Obtener las palabras ya procesadas desde la base de datos
    palabras = texto.palabras.all()[:10]  # Top 10
    
    print(f"Texto: {texto.titulo}")
    print(f"Total de palabras en BD: {texto.palabras.count()}")
    print(f"Mostrando: {palabras.count()} palabras")
    
    # Preparar datos para el template
    labels = [palabra.contenido for palabra in palabras]
    values = [palabra.frecuencia for palabra in palabras]
    
    return render(request, 'analisis/histograma.html', {
        'texto': texto,
        'palabras': palabras,
        'labels': labels,
        'values': values
    })

from collections import Counter
from nltk.util import ngrams
import nltk
import string

def ver_probabilidades(request, texto_id):
    """
    Muestra las tablas de frecuencias y probabilidades condicionales
    usando los n-gramas ya procesados y guardados en el modelo Palabra.
    """
    texto = get_object_or_404(TextoAnalizado, pk=texto_id)

    # Obtener los n-gramas guardados en la base de datos
    palabras = texto.palabras.all()  # Ya están ordenadas por frecuencia (-frecuencia)
    
    # Calcular la probabilidad MLE de cada n-grama
    if texto.n_grama > 1:
        # Para n-gramas mayores a 1, calcular probabilidad condicional
        # Agrupar por prefijo (todos excepto la última palabra)
        from collections import defaultdict

        prefix_counts = defaultdict(int)
        for p in palabras:
            tokens = p.contenido.split()
            prefix = ' '.join(tokens[:-1])
            prefix_counts[prefix] += p.frecuencia

        tabla = []
        for p in palabras:
            tokens = p.contenido.split()
            prefix = ' '.join(tokens[:-1])
            prob = p.frecuencia / prefix_counts[prefix] if prefix_counts[prefix] > 0 else 0
            tabla.append({
                'ngram': p.contenido,
                'frecuencia': p.frecuencia,
                'probabilidad': round(prob, 4)
            })
    else:
        # Para unigramas, probabilidad = frecuencia / total
        total = sum(p.frecuencia for p in palabras)
        tabla = [{
            'ngram': p.contenido,
            'frecuencia': p.frecuencia,
            'probabilidad': round(p.frecuencia / total, 4)
        } for p in palabras]

    contexto = {
        'texto': texto,
        'tabla': tabla,
        'n': texto.n_grama,
    }

    return render(request, 'analisis/probabilidades.html', contexto)

def calcular_probabilidades_con_fronteras(texto):
    """
    Recibe un objeto TextoAnalizado y devuelve una tabla de n-gramas con
    probabilidades condicionales incluyendo <s> y </s>.
    """
    import nltk
    from collections import Counter
    from nltk.util import ngrams

    # Tokenizar por oraciones
    contenido = ''
    with texto.archivo.open('rb') as f:
        try:
            contenido = f.read().decode('utf-8').lower()
        except UnicodeDecodeError:
            f.seek(0)
            contenido = f.read().decode('latin-1').lower()

    import string
    contenido = contenido.translate(str.maketrans('', '', string.punctuation + '¿¡'))

    sentences = nltk.sent_tokenize(contenido)
    tokens_fb = []
    for sent in sentences:
        words = nltk.word_tokenize(sent)
        tokens_fb.extend(['<s>'] + words + ['</s>'])

    n = texto.n_grama
    n_grams = list(ngrams(tokens_fb, n))
    ngram_freq = Counter(n_grams)
    if n > 1:
        prefix_freq = Counter([ngram[:-1] for ngram in n_grams])
        tabla = []
        for ngram, freq in ngram_freq.items():
            prefix = ngram[:-1]
            prob = freq / prefix_freq[prefix] if prefix_freq[prefix] > 0 else 0
            tabla.append({
                'ngram': ' '.join(ngram),
                'frecuencia': freq,
                'probabilidad': round(prob,4)
            })
    else:
        total = sum(ngram_freq.values())
        tabla = [{'ngram': ' '.join(ngram), 'frecuencia': freq, 'probabilidad': round(freq/total,4)} 
                for ngram, freq in ngram_freq.items()]

    return tabla

def ver_probabilidades_fronteras(request, texto_id):
    """
    Vista que muestra probabilidades condicionales usando n-gramas
    incluyendo las fronteras de oración <s> y </s>.
    """
    texto = get_object_or_404(TextoAnalizado, pk=texto_id)
    tabla = calcular_probabilidades_con_fronteras(texto)

    contexto = {
        'texto': texto,
        'tabla': tabla,
        'n': texto.n_grama,
    }

    return render(request, 'analisis/probabilidades.html', contexto)


