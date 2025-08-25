from django.contrib import admin
from .models import Impresora, Reserva

@admin.register(Impresora)
class ImpresoraAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'impresora', 'fecha', 'hora', 'estudiante_nombre', 'estado')
    list_filter  = ('impresora', 'fecha', 'estado')
    search_fields = ('estudiante_nombre', 'estudiante_cedula', 'estudiante_celular')
    autocomplete_fields = ('impresora',)
    date_hierarchy = 'fecha'
