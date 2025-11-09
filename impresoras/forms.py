from django import forms
from django.core.exceptions import ValidationError
from base.models import Persona   # ← trae las opciones

class PublicReservationForm(forms.Form):
    impresora_id = forms.IntegerField(widget=forms.HiddenInput)
    fecha = forms.DateField(widget=forms.HiddenInput)
    hora = forms.IntegerField(widget=forms.HiddenInput)

    estudiante_nombre  = forms.CharField(
        label="Nombre", 
        max_length=120,
        help_text="Ingrese nombre y apellido"
    )
    
    def clean_estudiante_nombre(self):
        nombre = self.cleaned_data.get('estudiante_nombre', '').strip()
        if nombre:
            partes = nombre.split()
            if len(partes) < 2:
                raise ValidationError("Por favor ingrese nombre y apellido.")
        return nombre
    
    estudiante_cedula  = forms.CharField(
        label="Cédula", 
        max_length=30, 
        required=False,
        widget=forms.TextInput(attrs={'pattern': '[0-9]*', 'inputmode': 'numeric'})
    )
    
    def clean_estudiante_cedula(self):
        cedula = self.cleaned_data.get('estudiante_cedula', '').strip()
        if cedula and not cedula.isdigit():
            raise ValidationError("La cédula solo puede contener números.")
        return cedula
    
    estudiante_celular = forms.CharField(
        label="Celular", 
        max_length=30, 
        required=False,
        widget=forms.TextInput(attrs={'pattern': '[0-9]*', 'inputmode': 'numeric'})
    )
    
    def clean_estudiante_celular(self):
        celular = self.cleaned_data.get('estudiante_celular', '').strip()
        if celular and not celular.isdigit():
            raise ValidationError("El celular solo puede contener números.")
        return celular
    
    # ↓ aquí el combo
    estudiante_carrera = forms.ChoiceField(label="Carrera", choices=Persona.CARRERAS)

class PublicLabReservationForm(forms.Form):
    fecha = forms.DateField(widget=forms.HiddenInput)
    hora = forms.IntegerField(widget=forms.HiddenInput)
    
    estudiante_nombre = forms.CharField(
        help_text="Ingrese nombre y apellido"
    )
    
    def clean_estudiante_nombre(self):
        nombre = self.cleaned_data.get('estudiante_nombre', '').strip()
        if nombre:
            partes = nombre.split()
            if len(partes) < 2:
                raise ValidationError("Por favor ingrese nombre y apellido.")
        return nombre
    
    estudiante_cedula = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'pattern': '[0-9]*', 'inputmode': 'numeric'})
    )
    
    def clean_estudiante_cedula(self):
        cedula = self.cleaned_data.get('estudiante_cedula', '').strip()
        if cedula and not cedula.isdigit():
            raise ValidationError("La cédula solo puede contener números.")
        return cedula
    
    estudiante_celular = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'pattern': '[0-9]*', 'inputmode': 'numeric'})
    )
    
    def clean_estudiante_celular(self):
        celular = self.cleaned_data.get('estudiante_celular', '').strip()
        if celular and not celular.isdigit():
            raise ValidationError("El celular solo puede contener números.")
        return celular
    
    estudiante_carrera = forms.ChoiceField(choices=Persona.CARRERAS)
    actividad = forms.CharField(
        label="Actividad a realizar",
        required=True,                 # ponlo False si quieres permitir vacío
        max_length=1000,
        widget=forms.Textarea(attrs={
            "rows": 3,
            "placeholder": "Escribe la actividad que vas a realizar en el laboratorio..."
        })
    )


