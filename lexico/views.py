import os
import uuid
from django.shortcuts import render
from django.conf import settings
from .forms import UploadFileForm
from .lexer import analizar_codigo

def index(request):
    form = UploadFileForm()
    return render(request, 'lexico/index.html', {'form': form})

def procesar_archivo(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            contenido = archivo.read().decode('utf-8')

            # Analizar el código completo línea por línea
            tokens_tabla = []  # para mostrar en la tabla
            tokens_salida = [] # para el archivo de salida

            for linea in contenido.splitlines():
                tokens_linea = analizar_codigo(linea)
                tokens_tabla.extend(tokens_linea)
                # Solo guardar los tokens reconocidos para el archivo, respetando líneas
                tokens_salida.append(" ".join([token for _, token in tokens_linea]))

            # Crear archivo de salida con saltos de línea
            salida_nombre = f"tokens_{uuid.uuid4().hex}.txt"
            salida_path = os.path.join(settings.MEDIA_ROOT, salida_nombre)
            os.makedirs(os.path.dirname(salida_path), exist_ok=True)

            with open(salida_path, "w", encoding="utf-8") as f:
                f.write("\n".join(tokens_salida))

            output_file = os.path.join(settings.MEDIA_URL.strip('/'), salida_nombre)

            return render(request, 'lexico/resultados.html', {
                'tokens': tokens_tabla,      # tabla para mostrar original/token
                'output_file': output_file   # archivo descargable solo con tokens
            })
    else:
        form = UploadFileForm()
    return render(request, 'lexico/index.html', {'form': form})
