import calendar
from datetime import date, timedelta, datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.formatting.rule import Rule
from openpyxl.styles.differential import DifferentialStyle
from django.utils import timezone
from django.utils import timezone  # ya lo tienes importado arriba

from io import BytesIO
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.styles import Font, Alignment, PatternFill
from django.utils import timezone

from io import BytesIO
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from django.utils import timezone

from io import BytesIO
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from django.utils import timezone



from .models import Impresora, Reserva, HOURS_RANGE
from .forms import PublicReservationForm
from django.shortcuts import redirect
from django.urls import reverse

from types import SimpleNamespace
from .models import Impresora, Reserva, LabReserva, HOURS_RANGE
from .forms import PublicReservationForm, PublicLabReservationForm

LAB_NAME = "Laboratorio Tech Factory"
LAB_CAPACITY = 15


# impresoras/templatetags/impresoras_extras.py
from django import template

register = template.Library()

# impresoras/templatetags/impresoras_extras.py
from django import template

register = template.Library()

# --- si ya tienes otras funciones/etiquetas, déjalas arriba ---



def lab_reservations_map(dias):
    """
    Devuelve un dict {(fecha, hora): {'count': N, 'items': [LabReserva,...]}}
    Solo cuenta reservas no canceladas.
    """
    qs = LabReserva.objects.filter(fecha__in=dias).exclude(estado='cancelado')
    bucket = {}
    for r in qs:
        key = (r.fecha, r.hora)
        bucket.setdefault(key, []).append(r)
    return {k: {'count': len(v), 'items': v} for k, v in bucket.items()}


from django.utils import timezone

def crear_reserva_lab(request):
    if request.method != "POST":
        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('impresoras:calendario')
        return redirect(next_url)

    form = PublicLabReservationForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Datos inválidos.")
        return redirect(request.POST.get('next') or "impresoras:calendario")

    f = form.cleaned_data["fecha"]   # date
    h = form.cleaned_data["hora"]    # int (0..23)

    # === BLOQUE NUEVO: no permitir fechas/horas pasadas ===
    today = timezone.localdate()
    now_hour = timezone.localtime().hour
    if f < today:
        messages.error(request, "No puedes reservar una fecha pasada.")
        return redirect(request.POST.get('next') or "impresoras:calendario")
    if f == today and h < now_hour:
        messages.error(request, "No puedes reservar una hora que ya pasó.")
        return redirect(request.POST.get('next') or "impresoras:calendario")
    # === FIN BLOQUE NUEVO ===

    # Validaciones: Lun–Vie y rango horario
    if f.weekday() > 4 or h not in HOURS_RANGE:
        messages.error(request, "Horario fuera de rango (Lun–Vie 08:00–21:00).")
        return redirect(request.POST.get('next') or "impresoras:calendario")

    # Cupos
    count = LabReserva.objects.filter(fecha=f, hora=h).exclude(estado='cancelado').count()
    if count >= LAB_CAPACITY:
        messages.error(request, "No hay cupos disponibles en esa franja.")
        return redirect(request.POST.get('next') or "impresoras:calendario")

    LabReserva.objects.create(
        fecha=f, hora=h,
        estudiante_nombre=form.cleaned_data["estudiante_nombre"],
        estudiante_cedula=form.cleaned_data["estudiante_cedula"],
        estudiante_celular=form.cleaned_data["estudiante_celular"],
        estudiante_carrera=form.cleaned_data["estudiante_carrera"],
        estado='reservado'
    )
    messages.success(request, "Reserva de laboratorio creada correctamente.")
    return redirect(request.POST.get('next') or "impresoras:calendario")


def _next(request, fallback_name: str):
    """
    Devuelve a dónde hay que volver:
    - POST.next (del modal)
    - GET.next (enlaces admin)
    - Referer del navegador
    - reverse(fallback_name) como último recurso
    """
    return (
        request.POST.get("next")
        or request.GET.get("next")
        or request.META.get("HTTP_REFERER")
        or reverse(fallback_name)
    )
# ----- utilidades -----
def monday_of_week(d: date) -> date:
    return d - timedelta(days=d.weekday())

def generate_week_days(pivot: date):
    monday = monday_of_week(pivot)
    return [monday + timedelta(days=i) for i in range(7)]  # Lun a dom

def reservations_map(impresora, dias):
    qs = Reserva.objects.filter(impresora=impresora, fecha__in=dias).exclude(estado='cancelado')
    return {(r.fecha, r.hora): r for r in qs}


# arriba del archivo
from django.db.models import Case, When, IntegerField

def list_impresoras():
    # 0 = impresoras, 1 = laboratorio → así el lab queda al final
    return list(
        Impresora.objects
        .annotate(
            is_lab=Case(
                When(nombre__iexact="Laboratorio Tech Factory", then=1),
                default=0,
                output_field=IntegerField(),
            )
        )
        .order_by('is_lab', 'nombre')
    )


from django.utils import timezone  # ← arriba con imports

# arriba del archivo (si aún no lo tienes)


from types import SimpleNamespace
from types import SimpleNamespace  # si no lo tienes ya importado

def _build_context(pivot_date: date, admin: bool):
    week_days = generate_week_days(pivot_date)
    impresoras = list_impresoras()

    tab_data = []
    for imp in impresoras:
        # ----- LAB -----
        if imp.nombre.strip().lower() == LAB_NAME.lower():
            # Mapa base: {(fecha, hora): {'count': N, 'items': [LabReserva,...]}}
            base = lab_reservations_map(week_days)

            # Normalizamos TODAS las celdas para la semana y calculamos all_used
            norm_mapa = {}
            for d in week_days:
                for h in HOURS_RANGE:
                    key = (d, h)
                    data = base.get(key, {'count': 0, 'items': []})
                    items = data.get('items', [])
                    count = int(data.get('count', 0) or 0)
                    all_used = (count > 0) and all(getattr(x, "estado", "") == "usado" for x in items)

                    # Usamos dict para que el template acceda como r.count / r.items / r.all_used
                    norm_mapa[key] = {
                        'count': count,
                        'items': items,
                        'all_used': all_used,
                    }

            mapa = norm_mapa
            is_lab = True

        # ----- IMPRESORAS -----
        else:
            # Deja exactamente como lo tenías: un solo objeto Reserva por celda (o None)
            mapa = reservations_map(imp, week_days)
            is_lab = False

        tab_data.append({"imp": imp, "mapa": mapa, "is_lab": is_lab})

    return {
        "week_days": week_days,
        "hours": HOURS_RANGE,
        "tab_data": tab_data,
        "is_admin": admin,
        "form": PublicReservationForm(),
        "lab_name": LAB_NAME,
        "lab_capacity": LAB_CAPACITY,
    }


# ----- PÚBLICO -----
def calendario_publico(request):
    week_str = request.GET.get("week")
    pivot = datetime.strptime(week_str, "%Y-%m-%d").date() if week_str else now().date()
    ctx = _build_context(pivot, admin=False)
    return render(request, "impresoras/calendario.html", ctx)

def crear_reserva(request):
    if request.method != "POST":
        return redirect(_next(request, "impresoras:calendario"))

    form = PublicReservationForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Datos inválidos.")
        return redirect(_next(request, "impresoras:calendario"))

    imp = get_object_or_404(Impresora, id=form.cleaned_data["impresora_id"])
    f = form.cleaned_data["fecha"]
    h = form.cleaned_data["hora"]

    today = timezone.localdate()
    now_hour = timezone.localtime().hour
    if f < today:
        messages.error(request, "No puedes reservar una fecha pasada.")
        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('impresoras:calendario')
        return redirect(next_url)
    if f == today and h < now_hour:
        messages.error(request, "No puedes reservar una hora que ya pasó.")
        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('impresoras:calendario')
        return redirect(next_url)

    # Si quieres permitir fin de semana, cambia esto por: if h not in HOURS_RANGE:
    if f.weekday() > 4 or h not in HOURS_RANGE:
        messages.error(request, "Horario fuera de rango (Lun–Vie 08:00–21:00).")
        return redirect(_next(request, "impresoras:calendario"))

    if Reserva.objects.filter(impresora=imp, fecha=f, hora=h).exists():
        messages.error(request, "Esa hora ya está reservada.")
        return redirect(_next(request, "impresoras:calendario"))

    Reserva.objects.create(
        impresora=imp,
        fecha=f,
        hora=h,
        estudiante_nombre=form.cleaned_data["estudiante_nombre"],
        estudiante_cedula=form.cleaned_data["estudiante_cedula"],
        estudiante_celular=form.cleaned_data["estudiante_celular"],
        estudiante_carrera=form.cleaned_data["estudiante_carrera"],
        estado='reservado'
    )
    messages.success(request, "Reserva creada correctamente.")
    return redirect(_next(request, "impresoras:calendario"))




@login_required
def exportar_excel_mes(request):
    import calendar
    from collections import defaultdict

    month_str = request.GET.get("month")           # "YYYY-MM"
    impresora_id = request.GET.get("impresora")    # puede venir vacío o ser un id

    if not month_str:
        messages.error(request, "Selecciona un mes (YYYY-MM).")
        return redirect("impresoras:calendario")

    try:
        y, m = map(int, month_str.split("-"))
        first = date(y, m, 1)
        last  = date(y, m, calendar.monthrange(y, m)[1])
    except Exception:
        messages.error(request, "Formato de mes inválido.")
        return redirect("impresoras:calendario")

    # Detecta IDs del laboratorio (por nombre, por si cambia)
    LAB_NAME = "Laboratorio Tech Factory"
    lab_ids = set(map(str, Impresora.objects
                      .filter(nombre__icontains="laboratorio")
                      .values_list("id", flat=True)))

    # ========= Construcción de datos =========
    rows_imp = []   # impresoras normales (hoja "Reservas")
    rows_lab = []   # detalle laboratorio (hoja "Detalle Lab")

    # ----- Caso 1: TODAS -----
    if not impresora_id:
        # Impresoras normales
        qs_imp = (Reserva.objects
                  .filter(fecha__range=(first, last))
                  .select_related("impresora")
                  .order_by("impresora__nombre", "fecha", "hora"))
        for r in qs_imp:
            creado_local = timezone.localtime(r.creado_en).replace(tzinfo=None)
            rows_imp.append((
                r.impresora.nombre, r.fecha,
                f"{r.hora:02d}:00 - {r.hora+1:02d}:00",
                r.get_estado_display(), r.estudiante_nombre,
                r.estudiante_cedula, r.estudiante_celular, r.estudiante_carrera,
                (getattr(r, "tecnico_observaciones", "") or "").replace("\r\n", " ").replace("\n", " ").strip(),
                creado_local,
            ))

        # Laboratorio
        qs_lab = (LabReserva.objects
                  .filter(fecha__range=(first, last))
                  .order_by("fecha", "hora", "estado", "estudiante_nombre"))
        for r in qs_lab:
            creado_local = timezone.localtime(r.creado_en).replace(tzinfo=None)
            rows_lab.append((
                LAB_NAME, r.fecha,
                f"{r.hora:02d}:00 - {r.hora+1:02d}:00",
                r.get_estado_display(), r.estudiante_nombre,
                r.estudiante_cedula, r.estudiante_celular, r.estudiante_carrera,
                (getattr(r, "tecnico_observaciones", "") or "").strip().replace("\r\n", " ").replace("\n", " "),
                creado_local,
                r.hora,              # columnas técnicas para resumen
                r.estado,
            ))

    # ----- Caso 2: SOLO LAB -----
    elif impresora_id in lab_ids:
        qs_lab = (LabReserva.objects
                  .filter(fecha__range=(first, last))
                  .order_by("fecha", "hora", "estado", "estudiante_nombre"))
        for r in qs_lab:
            creado_local = timezone.localtime(r.creado_en).replace(tzinfo=None)
            rows_lab.append((
                LAB_NAME, r.fecha,
                f"{r.hora:02d}:00 - {r.hora+1:02d}:00",
                r.get_estado_display(), r.estudiante_nombre,
                r.estudiante_cedula, r.estudiante_celular, r.estudiante_carrera,
                (getattr(r, "tecnico_observaciones", "") or "").strip().replace("\r\n", " ").replace("\n", " "),
                creado_local,
                r.hora,
                r.estado,
            ))

        # (Opcional) Si alguna vez guardaste reservas del lab en Reserva con ese id, las puedes incluir en "Reservas"
        qs_imp_lab = (Reserva.objects
                      .filter(fecha__range=(first, last), impresora_id=impresora_id)
                      .select_related("impresora")
                      .order_by("fecha", "hora"))
        for r in qs_imp_lab:
            creado_local = timezone.localtime(r.creado_en).replace(tzinfo=None)
            rows_imp.append((
                r.impresora.nombre, r.fecha,
                f"{r.hora:02d}:00 - {r.hora+1:02d}:00",
                r.get_estado_display(), r.estudiante_nombre,
                r.estudiante_cedula, r.estudiante_celular, r.estudiante_carrera,
                (getattr(r, "tecnico_observaciones", "") or "").replace("\r\n", " ").replace("\n", " ").strip(),
                creado_local,
            ))

    # ----- Caso 3: SOLO UNA IMPRESORA NORMAL -----
    else:
        qs_imp = (Reserva.objects
                  .filter(fecha__range=(first, last), impresora_id=impresora_id)
                  .select_related("impresora")
                  .order_by("impresora__nombre", "fecha", "hora"))
        for r in qs_imp:
            creado_local = timezone.localtime(r.creado_en).replace(tzinfo=None)
            rows_imp.append((
                r.impresora.nombre, r.fecha,
                f"{r.hora:02d}:00 - {r.hora+1:02d}:00",
                r.get_estado_display(), r.estudiante_nombre,
                r.estudiante_cedula, r.estudiante_celular, r.estudiante_carrera,
                (getattr(r, "tecnico_observaciones", "") or "").replace("\r\n", " ").replace("\n", " ").strip(),
                creado_local,
            ))

    # ========= Workbook =========
    wb = Workbook()
    ws_reservas = wb.active
    ws_reservas.title = "Reservas"

    # ---- Hoja 1: Reservas (impresoras normales + opcional lab si venía en Reserva) ----
    headers = [
        "Recurso", "Fecha", "Hora", "Estado",
        "Nombre", "Cédula", "Celular", "Carrera",
        "Observaciones", "Creado",
    ]
    ws_reservas.append(headers)
    for row in rows_imp:
        ws_reservas.append(row)

    # Formato fecha/hora de "Creado"
    for cell in ws_reservas["J"][1:]:
        if isinstance(cell.value, datetime):
            cell.number_format = "yyyy-mm-dd hh:mm"

    # Estilos
    header_fill = PatternFill("solid", fgColor="1F4E78")
    header_font = Font(color="FFFFFF", bold=True)
    for c in ws_reservas[1]:
        c.fill = header_fill
        c.font = header_font
        c.alignment = Alignment(horizontal="center", vertical="center")

    thin = Side(style="thin", color="DDDDDD")
    for row in ws_reservas.iter_rows(min_row=1, max_row=ws_reservas.max_row, min_col=1, max_col=len(headers)):
        for cell in row:
            cell.border = Border(top=thin, left=thin, right=thin, bottom=thin)

    # Auto ancho
    for col_cells in ws_reservas.columns:
        length = max(len(str(c.value)) if c.value is not None else 0 for c in col_cells)
        ws_reservas.column_dimensions[col_cells[0].column_letter].width = min(max(length + 2, 12), 40)

    # Table
    if ws_reservas.max_row > 1:
        table = Table(displayName="TablaReservas", ref=f"A1:J{ws_reservas.max_row}")
        table.tableStyleInfo = TableStyleInfo(
            name="TableStyleMedium9", showRowStripes=True, showColumnStripes=False
        )
        ws_reservas.add_table(table)
    else:
        ws_reservas["A2"] = "Sin reservas en el período/selector elegido."
        ws_reservas.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(headers))
        ws_reservas["A2"].alignment = Alignment(horizontal="center")
        ws_reservas["A2"].font = Font(italic=True, color="666666")

    # ========= Hojas del LAB (si corresponde) =========
    include_lab_sheets = (not impresora_id) or (impresora_id in lab_ids)
    if include_lab_sheets:
        # ---- Hoja 2: Detalle Lab ----
        ws_lab_det = wb.create_sheet("Detalle Lab")
        lab_headers = [
            "Recurso", "Fecha", "Hora", "Estado",
            "Nombre", "Cédula", "Celular", "Carrera",
            "Observaciones", "Creado",
        ]
        ws_lab_det.append(lab_headers)

        # Ordenamos Detalle: Fecha, Hora (num), Estado(Usado primero)
        # Ya viene ordenado, pero reforzamos
        estado_order = {"usado": 0, "reservado": 1}
        rows_lab_sorted = sorted(
            rows_lab,
            key=lambda x: (x[1], x[11], estado_order.get(x[12], 99), x[4] or "")
        )
        for r in rows_lab_sorted:
            # r = (..., creado_local, hora_num, estado)
            ws_lab_det.append(r[:10])  # sólo columnas visibles

        # Formato "Creado"
        for cell in ws_lab_det["J"][1:]:
            if isinstance(cell.value, datetime):
                cell.number_format = "yyyy-mm-dd hh:mm"

        # Estilo
        for c in ws_lab_det[1]:
            c.fill = header_fill
            c.font = header_font
            c.alignment = Alignment(horizontal="center", vertical="center")
        for row in ws_lab_det.iter_rows(min_row=1, max_row=ws_lab_det.max_row, min_col=1, max_col=len(lab_headers)):
            for cell in row:
                cell.border = Border(top=thin, left=thin, right=thin, bottom=thin)
        for col_cells in ws_lab_det.columns:
            length = max(len(str(c.value)) if c.value is not None else 0 for c in col_cells)
            ws_lab_det.column_dimensions[col_cells[0].column_letter].width = min(max(length + 2, 12), 40)

        if ws_lab_det.max_row > 1:
            t2 = Table(displayName="TablaDetalleLab", ref=f"A1:J{ws_lab_det.max_row}")
            t2.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
            ws_lab_det.add_table(t2)
        else:
            ws_lab_det["A2"] = "Sin reservas de laboratorio en el mes."
            ws_lab_det.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(lab_headers))
            ws_lab_det["A2"].alignment = Alignment(horizontal="center")
            ws_lab_det["A2"].font = Font(italic=True, color="666666")

        # ---- Hoja 3: Resumen Lab ----
        # Agrupa por (fecha, hora) => totales, usados, reservados
        resumen = defaultdict(lambda: {"total": 0, "usados": 0, "reservados": 0})
        for r in rows_lab:
            fecha = r[1]
            hora_num = r[11]  # columna técnica
            estado = (r[12] or "").lower()
            key = (fecha, hora_num)
            resumen[key]["total"] += 1
            if estado == "usado":
                resumen[key]["usados"] += 1
            elif estado == "reservado":
                resumen[key]["reservados"] += 1

        ws_lab_sum = wb.create_sheet("Resumen Lab")
        sum_headers = ["Fecha", "Hora", "Total", "Usados", "Reservados", "Cupo", "%Uso (Usados/Cupo)"]
        ws_lab_sum.append(sum_headers)

        for (fecha, hora_num) in sorted(resumen.keys()):
            tot = resumen[(fecha, hora_num)]["total"]
            usados = resumen[(fecha, hora_num)]["usados"]
            reservados = resumen[(fecha, hora_num)]["reservados"]
            cupo = LAB_CAPACITY  # del settings/constante
            # %Uso = usados / cupo
            pct = usados / cupo if cupo else 0
            ws_lab_sum.append([
                fecha,
                f"{hora_num:02d}:00 - {hora_num+1:02d}:00",
                tot, usados, reservados, cupo, pct
            ])

        # Estilo encabezado
        for c in ws_lab_sum[1]:
            c.fill = header_fill
            c.font = header_font
            c.alignment = Alignment(horizontal="center", vertical="center")

        # Formato %Uso
        for cell in ws_lab_sum["G"][1:]:
            if isinstance(cell.value, float):
                cell.number_format = "0.00%"

        # Bordes y anchos
        for row in ws_lab_sum.iter_rows(min_row=1, max_row=ws_lab_sum.max_row, min_col=1, max_col=len(sum_headers)):
            for cell in row:
                cell.border = Border(top=thin, left=thin, right=thin, bottom=thin)
        for col_cells in ws_lab_sum.columns:
            length = max(len(str(c.value)) if c.value is not None else 0 for c in col_cells)
            ws_lab_sum.column_dimensions[col_cells[0].column_letter].width = min(max(length + 2, 12), 32)

        if ws_lab_sum.max_row > 1:
            t3 = Table(displayName="TablaResumenLab", ref=f"A1:G{ws_lab_sum.max_row}")
            t3.tableStyleInfo = TableStyleInfo(name="TableStyleMedium4", showRowStripes=True)
            ws_lab_sum.add_table(t3)
        else:
            ws_lab_sum["A2"] = "Sin datos para el resumen de laboratorio."
            ws_lab_sum.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(sum_headers))
            ws_lab_sum["A2"].alignment = Alignment(horizontal="center")
            ws_lab_sum["A2"].font = Font(italic=True, color="666666")

    # ========= Respuesta =========
    bio = BytesIO()
    wb.save(bio)
    bio.seek(0)

    resp = HttpResponse(
        bio.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    resp["Content-Disposition"] = f'attachment; filename="reservas_{month_str}.xlsx"'
    return resp



# ----- ADMIN (con login) -----
@login_required
def calendario_admin(request):
    week_str = request.GET.get("week")
    pivot = datetime.strptime(week_str, "%Y-%m-%d").date() if week_str else now().date()
    ctx = _build_context(pivot, admin=True)
    return render(request, "impresoras/calendario.html", ctx)

@login_required
def admin_marcar_usado(request, pk):
    r = get_object_or_404(Reserva, pk=pk)

    if request.method == "POST":
        obs = request.POST.get("observaciones", "").strip()
        r.tecnico_observaciones = obs
        r.estado = "usado"
        r.save()
        messages.success(request, "Reserva marcada como usada.")
    else:
        # Fallback si alguien entra por GET
        if r.estado != "usado":
            r.estado = "usado"
            r.save()
            messages.success(request, "Reserva marcada como usada.")
        else:
            messages.info(request, "Esta reserva ya estaba marcada como usada.")

    next_url = request.GET.get('next') or request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('impresoras:admin_reservas')
    return redirect(next_url)

@login_required
def admin_cancelar_reserva(request, pk):
    r = get_object_or_404(Reserva, pk=pk)
    r.delete()  # ← elimina el registro para liberar el UNIQUE
    messages.success(request, "Reserva cancelada. La franja quedó libre.")
    # Vuelve a la página desde la que estabas (admin público)
    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER') or reverse('impresoras:admin_reservas')
    return redirect(_next(request, "impresoras:admin_reservas"))

    
@login_required
def admin_cancelar_lab(request, pk):
    r = get_object_or_404(LabReserva, pk=pk)
    r.delete()
    messages.success(request, "Reserva cancelada. La franja quedó libre.")
    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER') or reverse('impresoras:admin_reservas')
    return redirect(next_url)

@login_required
def admin_marcar_usado_lab(request, pk):
    r = get_object_or_404(LabReserva, pk=pk)
    if request.method == "POST":
        obs = request.POST.get("observaciones", "").strip()
        r.tecnico_observaciones = obs
        r.estado = "usado"
        r.save()
        messages.success(request, "Reserva marcada como usada.")
    else:
        if r.estado != "usado":
            r.estado = "usado"
            r.save()
            messages.success(request, "Reserva marcada como usada.")
        else:
            messages.info(request, "Esta reserva ya estaba marcada como usada.")
    next_url = request.GET.get('next') or request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('impresoras:admin_reservas')
    return redirect(next_url)



