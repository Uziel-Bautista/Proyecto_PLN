from django.shortcuts import render, redirect, get_object_or_404
from .forms import TextoAnalizadoForm
from .models import TextoAnalizado

def subir_texto(request):
    if request.method == 'POST':
        form = TextoAnalizadoForm(request.POST, request.FILES)
        if form.is_valid():
            texto = form.save()
            texto.procesar_texto()
            return redirect('lista_textos')
    else:
        form = TextoAnalizadoForm()
    return render(request, 'analisis/subir.html', {'form': form})

def lista_textos(request):
    textos = TextoAnalizado.objects.all().order_by('-fecha_subida')
    return render(request, 'analisis/lista.html', {'textos': textos})

def ver_histograma(request, texto_id):
    texto = get_object_or_404(TextoAnalizado, id=texto_id)
    palabras = texto.palabras.order_by('-frecuencia')
    return render(request, 'analisis/histograma.html', {'texto': texto, 'palabras': palabras})
