from django.db import models

class Producto(models.Model):
    UNIDADES_MEDIDA = [
        ('kg', 'Kilogramo'),
        ('unidad', 'Unidad'),
        ('caja', 'Caja'),
        ('paquete', 'Paquete'),
        ('litro', 'Litro'),
    ]
    
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150, verbose_name="Nombre del Producto")
    descripcion = models.CharField(max_length=191, verbose_name="Descripción", blank=True)
    precio_referencia = models.IntegerField(verbose_name="Precio de Venta")
    unidad_medida = models.CharField(
        max_length=20,
        choices=UNIDADES_MEDIDA,
        verbose_name="Unidad de Medida",
        help_text="Unidad en la que se vende el producto"
    )
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        db_table = "producto"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.get_unidad_medida_display()}) - ${self.precio_referencia:,}"
