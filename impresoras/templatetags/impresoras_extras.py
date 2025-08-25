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

