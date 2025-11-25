from django.db import models
from django.conf import settings

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    contacto = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)

    class Meta:
        db_table = 'cliente'

    def __str__(self):
        return self.nombre

class Auditoria(models.Model):
    ACCION_CHOICES = [
        ('CREAR', 'Crear'),
        ('EDITAR', 'Editar'),
        ('BORRAR', 'Borrar'),
    ]
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    accion = models.CharField(max_length=10, choices=ACCION_CHOICES)
    entidad = models.CharField(max_length=50)  # Ej: Usuario, Producto, Inventario
    detalle = models.TextField(blank=True)     # Ej: ID afectado, cambios, etc.

    def __str__(self):
        return f"{self.fecha_hora} - {self.usuario} - {self.accion} {self.entidad}"

    class Meta:
        verbose_name = "Evento de Auditoría"
        verbose_name_plural = "Eventos de Auditoría"
        db_table = "auditoria"
        ordering = ['-fecha_hora']
