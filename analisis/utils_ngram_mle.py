from collections import Counter
from nltk import word_tokenize
from nltk.util import ngrams

def calcular_probabilidades(texto, n=2, usar_fronteras=False):
    tokens = word_tokenize(texto.lower())
    if usar_fronteras:
        tokens = ['<s>'] + tokens + ['</s>']

    n_grams = list(ngrams(tokens, n))
    n_1_grams = list(ngrams(tokens, n-1)) if n > 1 else []

    freq_n = Counter(n_grams)
    freq_n1 = Counter(n_1_grams)

    resultados = []
    for gram, count in freq_n.items():
        if n == 1:
            prob = count / len(tokens)
        else:
            prob = count / freq_n1[gram[:-1]]
        resultados.append({
            'n_grama': ' '.join(gram),
            'frecuencia': count,
            'probabilidad': round(prob, 4)
        })
    return resultados
