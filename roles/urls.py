from django.urls import path
from . import views

app_name = 'roles'

urlpatterns = [
    path('', views.lista_roles, name='lista_roles'),
    path('crear/', views.crear_rol, name='crear_rol'),
    path('editar/<int:rol_id>/', views.editar_rol, name='editar_rol'),
    path('eliminar/<int:rol_id>/', views.eliminar_rol, name='eliminar_rol'),
]
