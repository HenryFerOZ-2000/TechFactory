from django.db import models
from base.models import Persona  # para Persona.CARRERAS

# Rango de horas permitido: 08..20 (cada bloque es 1h: 8-9, ..., 20-21)
HOURS_RANGE = list(range(8, 21))  # 8..20 inclusive

class Impresora(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    ESTADOS = (
        ('reservado', 'Reservado'),
        ('usado', 'Usado'),
        ('cancelado', 'Cancelado'),
    )
    impresora = models.ForeignKey(Impresora, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.PositiveIntegerField()  # 8..20
    estudiante_nombre = models.CharField(max_length=120)
    estudiante_cedula = models.CharField(max_length=30, blank=True, default="")
    estado = models.CharField(max_length=10, choices=ESTADOS, default='reservado')
    creado_en = models.DateTimeField(auto_now_add=True)
    estudiante_celular = models.CharField(max_length=30, blank=True, default="")
    estudiante_carrera = models.CharField(max_length=100, choices=Persona.CARRERAS, default=Persona.CARRERAS[0][0])
    tecnico_observaciones = models.TextField(blank=True, default="")  # ← NUEVO

    class Meta:
        unique_together = ('impresora', 'fecha', 'hora')  # evita doble reserva

    def __str__(self):
        return f"{self.impresora} {self.fecha} {self.hora}:00 ({self.estado})"


class LabReserva(models.Model):
    ESTADOS = (
        ('reservado', 'Reservado'),
        ('usado', 'Usado'),
        ('cancelado', 'Cancelado'),
    )
    # misma franja que impresoras
    fecha = models.DateField()
    hora = models.PositiveIntegerField()  # 8..20 (08–21)
    # datos de estudiante
    estudiante_nombre = models.CharField(max_length=120)
    estudiante_cedula = models.CharField(max_length=30, blank=True, default="")
    estudiante_celular = models.CharField(max_length=30, blank=True, default="")
    estudiante_carrera = models.CharField(max_length=100, choices=Persona.CARRERAS, default=Persona.CARRERAS[0][0])

    estado = models.CharField(max_length=10, choices=ESTADOS, default='reservado')
    creado_en = models.DateTimeField(auto_now_add=True)
    tecnico_observaciones = models.TextField(blank=True, default="")

    def __str__(self):
        return f"LAB {self.fecha} {self.hora:02d}:00 ({self.get_estado_display()})"
