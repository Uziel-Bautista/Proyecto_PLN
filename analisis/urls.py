from django.urls import path
from . import views

urlpatterns = [
    path('subir/', views.subir_texto, name='subir_texto'),
    path('', views.lista_textos, name='lista_textos'),
    path('histograma/<int:texto_id>/', views.ver_histograma, name='ver_histograma'),
    path('probabilidades/<int:texto_id>/', views.ver_probabilidades, name='ver_probabilidades'),
    path('probabilidades_fronteras/<int:texto_id>/', views.ver_probabilidades_fronteras, name='ver_probabilidades_fronteras'),


]

