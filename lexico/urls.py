from django.urls import path
from . import views

app_name = "lexico"

urlpatterns = [
    path('', views.index, name='index'),
    path('procesar/', views.procesar_archivo, name='procesar'),
]
