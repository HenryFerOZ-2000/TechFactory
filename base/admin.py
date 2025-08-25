from django.contrib import admin
from .models import Persona, Componente, Registro

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre','cedula','celular','carrera')
    search_fields = ('nombre','cedula','celular')

@admin.register(Componente)
class ComponenteAdmin(admin.ModelAdmin):
    list_display = ('nombre','ubicacion','cantidad_total','cantidad_disponible','activo','actualizado_en')
    list_filter = ('activo',)
    search_fields = ('nombre','ubicacion')

@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ('persona','componente','cantidad','estado','fecha_salida','fecha_entrada','vence_el','renovaciones')
    list_filter = ('estado','componente')
    search_fields = ('persona__nombre','persona__cedula')
