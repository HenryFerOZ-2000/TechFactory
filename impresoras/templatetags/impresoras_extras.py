from django import template
register = template.Library()

# SÍ: filtros de 1 arg
@register.filter
def dict_get(d, key):
    try:
        return d.get(key)
    except Exception:
        return None

# NUEVO: tag que acepta varios args
@register.simple_tag
def res_at(mapa, day, hour):
    """Devuelve mapa[(day, hour)] o None."""
    try:
        return mapa.get((day, hour))
    except Exception:
        return None

@register.simple_tag
def lab_at(mapa, d, h):
    """
    Devuelve dict {'count': N, 'items': [LabReserva,...]} para (fecha, hora)
    """
    return mapa.get((d, h), {'count': 0, 'items': []})

@register.filter(name="sub")
def sub(a, b):
    """
    Resta segura en plantillas: {{ a|sub:b }} => a - b
    Maneja None, strings numéricos y floats.
    """
    def to_num(x):
        try:
            return int(x)
        except (TypeError, ValueError):
            try:
                return float(x)
            except (TypeError, ValueError):
                return 0
    return to_num(a) - to_num(b)

@register.filter(name="is_past")
def is_past(date_obj, now_obj):
    """
    Compara si una fecha es anterior a la fecha/hora actual.
    Uso: {{ d|is_past:now }}
    Retorna True si la fecha es pasada.
    """
    if not date_obj or not now_obj:
        return False
    
    # Si now_obj es datetime, obtener solo la fecha
    if hasattr(now_obj, 'date'):
        now_date = now_obj.date()
    else:
        now_date = now_obj
    
    # Si date_obj es datetime, obtener solo la fecha
    if hasattr(date_obj, 'date'):
        date_only = date_obj.date()
    else:
        date_only = date_obj
    
    return date_only < now_date

@register.simple_tag
def is_past_time(date_obj, hour, now_obj):
    """
    Compara si una fecha/hora es pasada.
    Uso: {% is_past_time d h now %}
    Retorna True si la fecha es pasada o si es hoy pero la hora ya pasó.
    """
    if not date_obj or not now_obj:
        return False
    
    # Si now_obj es datetime, obtener fecha y hora
    if hasattr(now_obj, 'date'):
        now_date = now_obj.date()
        now_hour = now_obj.hour
    else:
        now_date = now_obj
        now_hour = 0
    
    # Si date_obj es datetime, obtener solo la fecha
    if hasattr(date_obj, 'date'):
        date_only = date_obj.date()
    else:
        date_only = date_obj
    
    # Convertir hour a int si es necesario
    try:
        hour_int = int(hour)
    except (TypeError, ValueError):
        hour_int = 0
    
    # Si la fecha es anterior, es pasada
    if date_only < now_date:
        return True
    
    # Si es el mismo día, verificar la hora
    if date_only == now_date:
        return hour_int < now_hour
    
    return False

