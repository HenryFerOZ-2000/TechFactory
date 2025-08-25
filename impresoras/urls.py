from django.urls import path
from . import views

app_name = "impresoras"

urlpatterns = [
    # PÚBLICO
    path("calendario/", views.calendario_publico, name="calendario"),
    path("crear/", views.crear_reserva, name="crear_reserva"),
    path("exportar-excel/", views.exportar_excel_mes, name="exportar_excel"),  # público si quieres

    # ADMIN (requiere login)
    path("admin/", views.calendario_admin, name="admin_reservas"),
    path("admin/cancelar/<int:pk>/", views.admin_cancelar_reserva, name="admin_cancelar"),
    path("admin/marcar-usado/<int:pk>/", views.admin_marcar_usado, name="admin_marcar_usado"),
    
    path("lab/crear/", views.crear_reserva_lab, name="crear_reserva_lab"),
    path("lab/admin/cancelar/<int:pk>/", views.admin_cancelar_lab, name="admin_cancelar_lab"),
    path("lab/admin/usado/<int:pk>/", views.admin_marcar_usado_lab, name="admin_marcar_usado_lab"),
]
