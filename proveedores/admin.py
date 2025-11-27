from django.contrib import admin
from .models import Proveedor


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
	list_display = ('id_proveedor', 'rut_nif', 'nombre', 'email', 'contacto', 'direccion')
	search_fields = ('rut_nif', 'nombre', 'email', 'contacto')
	list_per_page = 25
