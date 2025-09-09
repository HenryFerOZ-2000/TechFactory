from django.urls import path
from . import views

app_name = "impresoras"

urlpatterns = [
    # ----- PÚBLICO -----
    path("calendario/", views.calendario_publico, name="calendario"),
    path("crear/", views.crear_reserva, name="crear_reserva"),
    path("lab/crear/", views.crear_reserva_lab, name="crear_reserva_lab"),
    path("exportar-excel/", views.exportar_excel_mes, name="exportar_excel"),
    path("lab/exportar-excel/", views.exportar_excel_lab, name="exportar_excel_lab"),


    # ----- ADMIN -----
    path("admin/", views.calendario_admin, name="admin_reservas"),

    # Impresoras
    path("admin/cancelar/<int:pk>/", views.admin_cancelar_reserva, name="admin_cancelar"),
    path("admin/marcar-usado/<int:pk>/", views.admin_marcar_usado, name="admin_marcar_usado"),

    # Laboratorio
    path("lab/admin/cancelar/<int:pk>/", views.admin_cancelar_lab, name="admin_cancelar_lab"),
    path("lab/admin/usado/<int:pk>/", views.admin_marcar_usado_lab, name="admin_marcar_usado_lab"),
    path("lab/admin/penalizar/<int:lab_id>/", views.penalizar_lab, name="penalizar_lab"),

    # Buffer y penalizaciones (impresoras)
    path("reservas/<int:reserva_id>/penalizar/", views.penalizar_reserva, name="penalizar_reserva"),
    path("reservas/<int:reserva_id>/liberar-buffer/", views.liberar_buffer, name="liberar_buffer"),

    # ----- PENALIZADOS -----
    # Mismo path, misma vista, dos nombres (alias) para compatibilidad
    path("admin/penalizados/", views.penalizados_tabs, name="penalizados_tabs"),
    path("admin/penalizados/", views.penalizados_tabs, name="lista_penalizados"),

    # (opcionales) listas individuales
    path("admin/penalizados/impresoras/", views.lista_penalizados_imp, name="lista_penalizados_imp"),
    path("admin/penalizados/lab/", views.lista_penalizados_lab, name="lista_penalizados_lab"),
]
