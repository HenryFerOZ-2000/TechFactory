from django import forms
from .models import Persona, Componente  # <-- importa también Componente

class RegistroSalidaForm(forms.Form):
    nombre = forms.CharField()
    cedula = forms.CharField(label='Cédula')
    celular = forms.CharField(required=False)
    carrera = forms.ChoiceField(choices=Persona.CARRERAS)
    # ID real del componente (rellenado por el JS del datalist)
    componente_id = forms.IntegerField(widget=forms.HiddenInput())
    cantidad = forms.IntegerField(min_value=1)

class FiltroForm(forms.Form):
    filtro_cedula = forms.CharField(required=False)
    filtro_celular = forms.CharField(required=False)
    filtro_componente = forms.CharField(required=False)

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)

# >>> Form usado por el CRUD de Componentes (si lo tienes en las rutas/plantillas)
class ComponenteForm(forms.ModelForm):
    class Meta:
        model = Componente
        fields = ["nombre", "ubicacion", "cantidad_total", "cantidad_disponible", "activo"]
