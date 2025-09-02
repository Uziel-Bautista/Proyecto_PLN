# Procesamiento de Lenguaje Natural - Análisis de Textos

Sistema Django para análisis de textos y generación de histogramas de frecuencia de palabras, añadiendo en esta nueva version el analisis de textos en español, eliminando stopwords y símbolos de puntuación, y muestra las palabras más frecuentes en forma de histograma.

## Características

- Subida de archivos de texto (.txt)
- Análisis automático de frecuencia de palabras
- Generación de histogramas interactivos
- Procesamiento automático al guardar
- Conversión a minúsculas
- Eliminación de puntuación y caracteres especiales
- Filtrado de stopwords en español
- Interfaz web responsive
- Selección de tamaño de n-grama (1-20)
- Procesamiento automático con NLTK
- Histogramas interactivos con Chart.js
- Interfaz responsive con Bootstrap
- Detección automática de stopwords en español
- Visualización de top 10 n-gramas

## Requisitos

- Python 3.8+
- pipnv (entorno virtual)
- git

## Instalación

1. Clonar el repositorio
git clone [https://github.com/Uziel-Bautista/Proyecto_PLN.git]
cd [PROCESAMIENTO DE LENGUAJE NATURAL]

2. Configurar entorno virtual con Pipenv
# Instalar pipenv si no está instalado
pip install pipenv
# Crear entorno virtual e instalar dependencias
pipenv install

3. Instalar dependencias del sistema (si es necesario)
# Para Ubuntu/Debian
sudo apt-get install python3-dev
# Para macOS con Homebrew
brew install python



## Ejecución

1. Activar entorno virtual
pipenv shell

2. Configurar base de datos
python manage.py migrate

3. Crear superusuario (opcional)
python manage.py createsuperuser

4. Ejecutar servidor
python manage.py runserver

5. Abrir en el navegador
Abrir en el navegador: http://127.0.0.1:8000/

Uso del Sistema
Subir texto: Click en "Subir nuevo texto"

Seleccionar archivo: Elegir archivo .txt desde tu computadora

Elegir n-grama: Ingresar un número entre 1 y 20 (ej: 2 para bigramas, 3 para trigramas)

Procesar: El sistema analizará automáticamente el texto

Ver resultados: Click en "Ver histograma" para ver la visualización


Notas Importantes
Primera Ejecución
La primera vez que se ejecute, el sistema descargará automáticamente los recursos de NLTK

Esto puede tomar 1-2 minutos

Se creará la carpeta nltk_data/ automáticamente

Formatos de Archivo
Solo se aceptan archivos de texto (.txt)

El sistema soporta codificación UTF-8 y Latin-1

Recursos NLTK
El sistema requiere estos recursos de NLTK:

punkt - Tokenizador

punkt_tab - Tokenizador con tabulaciones

stopwords - Palabras vacías en español