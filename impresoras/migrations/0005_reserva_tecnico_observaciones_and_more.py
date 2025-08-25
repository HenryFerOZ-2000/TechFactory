from django.db import migrations

def seed_lab(apps, schema_editor):
    Impresora = apps.get_model('impresoras', 'Impresora')
    Impresora.objects.get_or_create(nombre='Laboratorio Tech Factory')

def unseed_lab(apps, schema_editor):
    Impresora = apps.get_model('impresoras', 'Impresora')
    Impresora.objects.filter(nombre='Laboratorio Tech Factory').delete()

class Migration(migrations.Migration):

    dependencies = [
        # Apunta a tu última migración real de la app impresoras
        ('impresoras', '0004_seed_printers'),  # cambia si tu último nombre es otro
    ]

    operations = [
        migrations.RunPython(seed_lab, reverse_code=unseed_lab),
    ]
