from django.urls import path
from . import views

app_name = 'proveedores'

urlpatterns = [
    path('', views.lista_proveedores, name='lista_proveedores'),
    path('formulario/', views.form_proveedor, name='form_proveedor'),
    path('agregar/', views.agregar_proveedor, name='agregar_proveedor'),
    path('editar/<int:proveedor_id>/', views.editar_proveedor, name='editar_proveedor'),
    path('eliminar/<int:proveedor_id>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    path('exportar-excel/', views.exportar_proveedores_excel, name='exportar_proveedores_excel'),
]