from django import forms
from .models import Justificacion

class JustificacionForm(forms.ModelForm):
    class Meta:
        model = Justificacion
        fields = ['fecha_inasistencia', 'motivo', 'descripcion', 'documento']
        widgets = {
            'fecha_inasistencia': forms.DateInput(attrs={'type': 'date'}),
        }
