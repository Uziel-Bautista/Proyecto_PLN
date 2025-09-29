from django import forms

class UploadFileForm(forms.Form):
    archivo = forms.FileField(label="Selecciona un archivo (.py o .txt)")
