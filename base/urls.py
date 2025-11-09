from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    # Auth simple (login único)
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Home
    path('', views.landing, name='landing'),                 # ← PÚBLICO
    path('inventario/', views.index, name='index'),          # ← PROTEGIDO (tu tabla)

    # Registros
    path('registrar_salida/', views.registrar_salida, name='registrar_salida'),
    path('registrar_entrada/<int:registro_id>/', views.registrar_entrada, name='registrar_entrada'),
    path('renovar_salida/<int:registro_id>/', views.renovar_salida, name='renovar_salida'),
    path('generar_correo/<int:registro_id>/', views.generar_correo, name='generar_correo'),
    path('eliminar_registro/<int:registro_id>/', views.eliminar_registro, name='eliminar_registro'),
    path('exportar_excel/', views.exportar_excel, name='exportar_excel'),
    path('limpiar_todo/', views.limpiar_todo, name='limpiar_todo'),

    # Componentes (CRUD)
    path('componentes/', views.componentes_list, name='componentes_list'),
    path('componentes/crear/', views.componentes_create, name='componentes_create'),
    path('componentes/<int:comp_id>/editar/', views.componentes_edit, name='componentes_edit'),
    path('componentes/<int:comp_id>/toggle-activo/', views.componentes_toggle_activo, name='componentes_toggle_activo'),
    path('componentes/<int:comp_id>/eliminar/', views.componentes_delete, name='componentes_delete'),

    # CSV
    path('importar_csv/', views.importar_csv, name='importar_csv'),
    path('descargar_plantilla_csv/', views.descargar_plantilla_csv, name='descargar_plantilla_csv'),
    path('cargar_inventario/', views.cargar_inventario, name='cargar_inventario'),
    path('informe_vencidos/', views.informe_vencidos, name='informe_vencidos'),
]

