from django import forms
from base.models import Persona   # ← trae las opciones

class PublicReservationForm(forms.Form):
    impresora_id = forms.IntegerField(widget=forms.HiddenInput)
    fecha = forms.DateField(widget=forms.HiddenInput)
    hora = forms.IntegerField(widget=forms.HiddenInput)

    estudiante_nombre  = forms.CharField(label="Nombre", max_length=120)
    estudiante_cedula  = forms.CharField(label="Cédula", max_length=30, required=False)
    estudiante_celular = forms.CharField(label="Celular", max_length=30, required=False)
    # ↓ aquí el combo
    estudiante_carrera = forms.ChoiceField(label="Carrera", choices=Persona.CARRERAS)

class PublicLabReservationForm(forms.Form):
    fecha = forms.DateField(widget=forms.HiddenInput)
    hora = forms.IntegerField(widget=forms.HiddenInput)
    estudiante_nombre = forms.CharField()
    estudiante_cedula = forms.CharField(required=False)
    estudiante_celular = forms.CharField(required=False)
    estudiante_carrera = forms.ChoiceField(choices=Persona.CARRERAS)

