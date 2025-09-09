from django.db import models
from django.utils import timezone
from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.utils import timezone


# models.py
class Persona(models.Model):
    CARRERAS = [
        ('Robotica e IA', 'Robotica e IA'),
        ('Sistemas Biomedicos', 'Sistemas Biomedicos'),
        ('Sistemas Computacionales', 'Sistemas Computacionales'),
        ('Software', 'Software'),
        ('Realidad Virtual Y videojuegos', 'Realidad Virtual Y videojuegos'),
        ('Transformacion Digital de Negocios', 'Transformacion Digital de Negocios'),
    ]
    nombre = models.CharField(max_length=120)
    cedula = models.CharField(max_length=20)
    celular = models.CharField(max_length=20, blank=True, default='')
    carrera = models.CharField(max_length=120, choices=CARRERAS)

    # NUEVO (no quites penalized_until si ya existe/lo usabas en otros lados)
    penalizado_impresoras_hasta = models.DateTimeField(null=True, blank=True)
    penalizado_lab_hasta = models.DateTimeField(null=True, blank=True)

    no_show_count = models.PositiveIntegerField(default=0)
    penalized_until = models.DateTimeField(null=True, blank=True)  # legado si ya lo tenías

    def __str__(self):
        return f"{self.nombre} ({self.cedula})"


class Componente(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    ubicacion = models.CharField(max_length=200, blank=True, default='')
    cantidad_total = models.PositiveIntegerField(default=0)
    cantidad_disponible = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Registro(models.Model):
    ESTADOS = (('prestado', 'Prestado'), ('devuelto', 'Devuelto'))
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    componente = models.ForeignKey(Componente, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_salida = models.DateTimeField(default=timezone.now)
    fecha_entrada = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=12, choices=ESTADOS, default='prestado')
    renovaciones = models.PositiveIntegerField(default=0)
    vence_el = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-fecha_salida']

    def __str__(self):
        return f"{self.persona} - {self.componente} x{self.cantidad}"
