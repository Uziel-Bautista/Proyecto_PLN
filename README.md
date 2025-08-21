# Procesamiento de Lenguaje Natural - Análisis de Textos

Sistema Django para análisis de textos y generación de histogramas de frecuencia de palabras.

## Características

- Subida de archivos de texto (.txt)
- Análisis automático de frecuencia de palabras
- Generación de histogramas interactivos
- Interfaz administrativa Django

## Requisitos

- Python 3.8+
- pip
- virtualenv (recomendado)

## Instalación

1. Clonar el repositorio:
```bash
git clone [https://github.com/Uziel-Bautista/Proyecto_PLN.git]
cd Procesamiento_de_lenguaje_natural

2. Crear Entorno Virtual (Recomendado)
Windows:


python -m venv venv
venv\Scripts\activate
Linux/Mac:


python3 -m venv venv
source venv/bin/activate


3. Instalar Dependencias

pip install -r requirements.txt


4. Configurar la Base de Datos

python manage.py migrate


5. Crear Usuario Administrador (Opcional)
bash
python manage.py createsuperuser
Siga las instrucciones para crear un usuario admin


6. Ejecutar el Servidor

python manage.py runserver
🌐 Acceso a la Aplicación
Interfaz Principal: http://127.0.0.1:8000/

Admin Django: http://127.0.0.1:8000/admin/

Subir Textos: http://127.0.0.1:8000/subir/

📖 Manual de Uso
Para Usuarios Regulares
Acceder a la aplicación en http://127.0.0.1:8000/

Hacer clic en "Subir nuevo texto"

Seleccionar un archivo .txt desde tu computadora

Hacer clic en "Enviar" - el sistema procesará automáticamente el texto

Ver la lista de textos con sus palabras y frecuencias

Hacer clic en "Ver histograma" para visualización gráfica

Para Administradores
Acceder al admin en http://127.0.0.1:8000/admin/

Iniciar sesión con las credenciales de superusuario

Gestionar textos (crear, editar, eliminar)

Ver estadísticas de palabras y frecuencias