from django.db import models
from productos.models import Producto

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
