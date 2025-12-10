from django.db import models
from productos.models import Producto
from django.conf import settings
from django.utils import timezone

class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Producto")
    cantidad_actual = models.IntegerField(verbose_name="Cantidad Actual")
    stock_minimo = models.IntegerField(
        verbose_name="Stock Mínimo",
        help_text="Cantidad mínima requerida en inventario"
    )
    stock_maximo = models.IntegerField(
        verbose_name="Stock Máximo",
        null=True,
        blank=True,
        help_text="Cantidad máxima permitida (opcional)"
    )
    ubicacion = models.CharField(max_length=150, verbose_name="Ubicación")
    fecha_ultima_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    
    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
        db_table = "inventario"
        ordering = ['-fecha_ultima_actualizacion']
        unique_together = ['id_producto', 'ubicacion']
    
    def __str__(self):
        return f"{self.id_producto.nombre} - {self.ubicacion}: {self.cantidad_actual} unidades"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.cantidad_actual < 0:
            raise ValidationError("La cantidad actual no puede ser negativa.")
        if self.stock_minimo < 0:
            raise ValidationError("El stock mínimo no puede ser negativo.")
        if self.stock_maximo is not None and self.stock_maximo < self.stock_minimo:
            raise ValidationError("El stock máximo no puede ser menor que el stock mínimo.")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class MovimientoInventario(models.Model):
    TIPO_CHOICES = (
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    )

    id_movimiento = models.AutoField(primary_key=True)
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE, related_name='movimientos')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.PositiveIntegerField()
    proveedor = models.CharField(max_length=255, blank=True)
    motivo = models.CharField(max_length=255, blank=True)
    detalle = models.TextField(blank=True)
    stock_resultante = models.IntegerField()
    fecha_hora = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'movimiento_inventario'
        ordering = ['-fecha_hora']
        verbose_name = 'Movimiento de Inventario'
        verbose_name_plural = 'Movimientos de Inventario'

    def __str__(self):
        signo = '+' if self.tipo == 'entrada' else '-'
        return f"{self.get_tipo_display()} {signo}{self.cantidad} de {self.inventario.id_producto.nombre}"
