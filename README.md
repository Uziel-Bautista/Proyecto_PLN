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


## Configuración

1. Configurar base de datos
# Aplicar migraciones
pipenv run python manage.py migrate

2. Descargar recursos de NLTK
# Ejecutar shell de Django
pipenv run python manage.py shell
# En el shell, ejecutar:
import nltk
nltk.download('stopwords')
exit()

3. Crear superusuario (opcional)
pipenv run python manage.py createsuperuser

## Ejecución

1. Iniciar servidor de desarrollo
pipenv run python manage.py runserver

2. Acceder a la aplicación
Abrir en el navegador: http://127.0.0.1:8000/