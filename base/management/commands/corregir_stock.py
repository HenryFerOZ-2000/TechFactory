# base/management/commands/corregir_stock.py
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from base.models import Componente, Registro


class Command(BaseCommand):
    help = (
        "Devuelve al stock (cantidad_disponible) las unidades de todos los registros "
        "que siguen 'prestado'. Opcionalmente marca esos registros como devueltos."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--marcar-devueltos",
            action="store_true",
            help="Además de devolver el stock, marca los registros abiertos como devueltos y setea fecha_entrada=now().",
        )

    def handle(self, *args, **opts):
        # Agrupamos lo prestado por componente para ajustar de golpe
        with transaction.atomic():
            agregados = (
                Registro.objects
                .filter(estado="prestado")
                .values("componente")
                .annotate(total=Sum("cantidad"))
            )

            ajustados = 0
            for row in agregados:
                comp_id = row["componente"]
                total_prestado = row["total"] or 0
                comp = Componente.objects.filter(id=comp_id).first()
                if not comp or total_prestado <= 0:
                    continue

                comp.cantidad_disponible = (comp.cantidad_disponible or 0) + total_prestado
                comp.save(update_fields=["cantidad_disponible"])
                ajustados += 1
                self.stdout.write(f"✓ {comp.nombre}: +{total_prestado} → disp={comp.cantidad_disponible}")

            if opts.get("marcar_devueltos"):
                n = (
                    Registro.objects
                    .filter(estado="prestado")
                    .update(estado="devuelto", fecha_entrada=timezone.now())
                )
                self.stdout.write(f"Registros marcados como devueltos: {n}")

        self.stdout.write(self.style.SUCCESS(f"Listo. Componentes ajustados: {ajustados}"))
