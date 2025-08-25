from django.db import migrations

def seed_printers(apps, schema_editor):
    Impresora = apps.get_model('impresoras', 'Impresora')
    for nombre in ["Creality K1 Max", "Raise3D E2"]:
        Impresora.objects.get_or_create(nombre=nombre)

def unseed_printers(apps, schema_editor):
    Impresora = apps.get_model('impresoras', 'Impresora')
    Impresora.objects.filter(nombre__in=["Creality K1 Max", "Raise3D E2"]).delete()

class Migration(migrations.Migration):

    dependencies = [
        # Debe apuntar a tu última migración previa:
        ('impresoras', '0003_alter_reserva_estudiante_carrera'),  # <-- ESTE NOMBRE
    ]

    operations = [
        migrations.RunPython(seed_printers, reverse_code=unseed_printers),
    ]
