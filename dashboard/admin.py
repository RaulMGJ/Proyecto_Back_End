from django.contrib import admin
from .models import Auditoria

@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ('fecha_hora', 'usuario', 'accion', 'entidad', 'detalle')
    list_filter = ('accion', 'entidad', 'usuario')
    search_fields = ('detalle', 'usuario__username', 'usuario__nombre')
    date_hierarchy = 'fecha_hora'
    ordering = ('-fecha_hora',)
