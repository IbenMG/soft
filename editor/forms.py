from django import forms
from .models import Boletin

class BoletinForm(forms.ModelForm):
    class Meta:
        model = Boletin
        fields = ['titulo', 'contenido_html', 'imagen_destacada', 'esta_publicado', 'es_plantilla']
        widgets = {
            'contenido_html': forms.Textarea(attrs={'id': 'id_contenido'}),
        }
