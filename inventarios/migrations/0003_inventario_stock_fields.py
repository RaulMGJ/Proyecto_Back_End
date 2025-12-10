# Generated manually to add stock_minimo y stock_maximo a inventario
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventarios', '0002_movimientoinventario'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventario',
            name='stock_minimo',
            field=models.IntegerField(default=0, verbose_name='Stock Mínimo', help_text='Cantidad mínima requerida en inventario'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventario',
            name='stock_maximo',
            field=models.IntegerField(blank=True, help_text='Cantidad máxima permitida (opcional)', null=True, verbose_name='Stock Máximo'),
        ),
    ]
