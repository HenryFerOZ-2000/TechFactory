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
        ('penalizado', 'Penalizado'),   # ← NUEVO
        ('cancelado', 'Cancelado'),
    )

    # Distinguir reservas normales vs margen de 1h
    TIPO = (
        ('NORMAL', 'Normal'),
        ('BUFFER', 'Buffer 1h'),
    )

    impresora = models.ForeignKey(Impresora, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.PositiveIntegerField()  # 8..20

    # datos del estudiante
    estudiante_nombre = models.CharField(max_length=120)
    estudiante_cedula = models.CharField(max_length=30, blank=True, default="")
    estudiante_celular = models.CharField(max_length=30, blank=True, default="")
    estudiante_carrera = models.CharField(
        max_length=100,
        choices=Persona.CARRERAS,
        default=Persona.CARRERAS[0][0]
    )

    # estado / metadatos
    estado = models.CharField(max_length=12, choices=ESTADOS, default='reservado')
    creado_en = models.DateTimeField(auto_now_add=True)
    tecnico_observaciones = models.TextField(blank=True, default="")

    # margen automático
    tipo = models.CharField(max_length=10, choices=TIPO, default='NORMAL')
    parent = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='buffers'
    )

    class Meta:
        unique_together = ('impresora', 'fecha', 'hora')  # evita doble reserva
        indexes = [
            models.Index(fields=['impresora', 'fecha', 'hora']),
            models.Index(fields=['fecha', 'hora']),
        ]

    def __str__(self):
        return f"{self.impresora} {self.fecha} {self.hora}:00 ({self.estado}, {self.tipo})"

    # --------- Helpers para el margen (BUFFER) ---------
    def siguiente_hora(self):
        """Devuelve la siguiente hora si está dentro del rango permitido; si no, None."""
        nxt = self.hora + 1
        return nxt if nxt in HOURS_RANGE else None

    def slot_buffer(self):
        """
        Retorna (fecha, siguiente_hora) si hay una hora siguiente válida.
        El buffer siempre es MISMO DÍA y hora+1 en este diseño.
        """
        nxt = self.siguiente_hora()
        if nxt is None:
            return None
        return (self.fecha, nxt)

    def puede_crear_buffer(self) -> bool:
        """True si existe la hora siguiente y no está ocupada en la misma impresora/fecha."""
        slot = self.slot_buffer()
        if slot is None:
            return False
        f, h = slot
        return not Reserva.objects.filter(
            impresora=self.impresora,
            fecha=f,
            hora=h
        ).exists()


class LabReserva(models.Model):
    ESTADOS = (
        ('reservado', 'Reservado'),
        ('usado', 'Usado'),
        ('penalizado', 'Penalizado'),   # ← NUEVO
        ('cancelado', 'Cancelado'),
    )

    # misma franja que impresoras
    fecha = models.DateField()
    hora = models.PositiveIntegerField()  # 8..20 (08–21)

    # datos de estudiante
    estudiante_nombre = models.CharField(max_length=120)
    estudiante_cedula = models.CharField(max_length=30, blank=True, default="")
    estudiante_celular = models.CharField(max_length=30, blank=True, default="")
    estudiante_carrera = models.CharField(
        max_length=100,
        choices=Persona.CARRERAS,
        default=Persona.CARRERAS[0][0]
    )

    estado = models.CharField(max_length=12, choices=ESTADOS, default='reservado')
    creado_en = models.DateTimeField(auto_now_add=True)
    tecnico_observaciones = models.TextField(blank=True, default="")

    class Meta:
        indexes = [
            models.Index(fields=['fecha', 'hora']),
        ]

    def __str__(self):
        return f"LAB {self.fecha} {self.hora:02d}:00 ({self.get_estado_display()})"
    

class Penalizacion(models.Model):
    AMBITOS = [
        ("impresoras", "Impresoras"),
        ("laboratorio", "Laboratorio"),
    ]

    persona = models.ForeignKey("base.Persona", on_delete=models.CASCADE, related_name="penalizaciones")
    ambito = models.CharField(max_length=20, choices=AMBITOS)
    hasta = models.DateTimeField()

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.persona} - {self.ambito} hasta {self.hasta}"

    
