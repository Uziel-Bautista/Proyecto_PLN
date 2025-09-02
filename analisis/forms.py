from django import forms
from .models import TextoAnalizado

class TextoAnalizadoForm(forms.ModelForm):
    n_grama = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=2,
        label="Tamaño del n-grama",
        help_text="Introduce un número entre 1 y 20",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 2 para bigramas, 3 para trigramas'
        })
    )

    class Meta:
        model = TextoAnalizado
        fields = ['archivo', 'n_grama']
        widgets = {
            'archivo': forms.FileInput(attrs={'class': 'form-control'})
        }

