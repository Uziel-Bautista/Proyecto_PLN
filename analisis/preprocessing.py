import string
from nltk.corpus import stopwords

# Si es la primera vez que usas nltk.stopwords, asegúrate de descargar:
# import nltk
# nltk.download('stopwords')

def limpiar_texto(texto):
    # 1. Convertir a minúsculas
    texto = texto.lower()

    # 2. Eliminar puntuación
    texto = texto.translate(str.maketrans('', '', string.punctuation))

    # 3. Eliminar stopwords en español
    stop_words = set(stopwords.words('spanish'))
    tokens = texto.split()
    tokens_limpios = [t for t in tokens if t not in stop_words]

    return tokens_limpios
