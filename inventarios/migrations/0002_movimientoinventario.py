# Generated manually to add MovimientoInventario model
from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inventarios', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MovimientoInventario',
            fields=[
                ('id_movimiento', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(choices=[('entrada', 'Entrada'), ('salida', 'Salida')], max_length=10)),
                ('cantidad', models.PositiveIntegerField()),
                ('proveedor', models.CharField(blank=True, max_length=255)),
                ('motivo', models.CharField(blank=True, max_length=255)),
                ('detalle', models.TextField(blank=True)),
                ('stock_resultante', models.IntegerField()),
                ('fecha_hora', models.DateTimeField(default=django.utils.timezone.now)),
                ('inventario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movimientos', to='inventarios.inventario')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Movimiento de Inventario',
                'verbose_name_plural': 'Movimientos de Inventario',
                'db_table': 'movimiento_inventario',
                'ordering': ['-fecha_hora'],
            },
        ),
    ]
