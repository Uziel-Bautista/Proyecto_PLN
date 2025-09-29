import re

# ------------------------------
# Árbol Binario de Búsqueda (ABB) para palabras reservadas
# ------------------------------
class NodoABB:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None

class ABB:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        def _insertar(nodo, valor):
            if not nodo:
                return NodoABB(valor)
            if valor < nodo.valor:
                nodo.izq = _insertar(nodo.izq, valor)
            elif valor > nodo.valor:
                nodo.der = _insertar(nodo.der, valor)
            return nodo
        self.raiz = _insertar(self.raiz, valor)

    def buscar(self, valor):
        def _buscar(nodo, valor):
            if not nodo:
                return False
            if nodo.valor == valor:
                return True
            if valor < nodo.valor:
                return _buscar(nodo.izq, valor)
            return _buscar(nodo.der, valor)
        return _buscar(self.raiz, valor)

# ------------------------------
# Palabras reservadas
# ------------------------------
reservadas = [
    "if", "else", "for", "while", "def", "return", "class", "import",
    "from", "as", "with", "try", "except", "finally", "break",
    "continue", "pass", "True", "False", "None"
]

abb = ABB()
for palabra in reservadas:
    abb.insertar(palabra)

# ------------------------------
# Símbolos y operadores con tokens claros
# ------------------------------
simbolos = {
    '(': 'PI', ')': 'PD', '{': 'LLI', '}': 'LLD', '[': 'CA', ']': 'CC',
    '=': 'IG', '+': 'MAS', '-': 'MENOS', '*': 'POR', '/': 'DIV', ':': 'DOSP',
    ',': 'COMA', '.': 'PTO'
}

# ------------------------------
# Función de análisis léxico
# ------------------------------
def analizar_codigo(codigo):
    """
    Devuelve lista de tuplas (token original, token reconocido)
    manteniendo el orden exacto del código.
    """
    resultado = []

    # Patrón general para comentarios, strings, números, identificadores y símbolos
    patron = re.compile(
        r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|#.*?$|"[^"\n]*"|\'[^\']*\'|[a-zA-Z_][a-zA-Z0-9_]*|\d+(\.\d+)?|[\(\)\{\}\[\]=+\-*/:,.])',
        re.MULTILINE
    )

    for match in patron.finditer(codigo):
        token = match.group()
        # Comentarios
        if token.startswith(('"""', "'''", "#")):
            tipo = "COM"
        # Palabras reservadas
        elif abb.buscar(token):
            tipo = "PR"
        # Números
        elif re.fullmatch(r'\d+(\.\d+)?', token):
            tipo = "NUM"
        # Identificadores
        elif re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_]*', token):
            tipo = "VAR"
        # Strings
        elif token.startswith(("'", '"')):
            tipo = "STR"
        # Símbolos y operadores
        else:
            tipo = simbolos.get(token, token)
        resultado.append((token, tipo))

    return resultado
