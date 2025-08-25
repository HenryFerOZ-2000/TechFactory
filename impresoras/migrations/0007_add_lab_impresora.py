from django.db import migrations

def add_lab(apps, schema_editor):
    Impresora = apps.get_model('impresoras', 'Impresora')
    Impresora.objects.get_or_create(nombre='Laboratorio Tech Factory')

def remove_lab(apps, schema_editor):
    Impresora = apps.get_model('impresoras', 'Impresora')
    Impresora.objects.filter(nombre='Laboratorio Tech Factory').delete()

class Migration(migrations.Migration):

    dependencies = [
    ('impresoras', '0006_labreserva'),   # en vez de 0005_..

   ]


    operations = [
        migrations.RunPython(add_lab, reverse_code=remove_lab),
    ]
