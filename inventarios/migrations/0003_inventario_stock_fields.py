# Generated manually to add stock_minimo y stock_maximo a inventario
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventarios', '0002_movimientoinventario'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="ALTER TABLE inventario ADD COLUMN IF NOT EXISTS stock_minimo INTEGER NOT NULL DEFAULT 0;",
                    reverse_sql="ALTER TABLE inventario DROP COLUMN IF EXISTS stock_minimo;",
                ),
            ],
            state_operations=[
                migrations.AddField(
                    model_name='inventario',
                    name='stock_minimo',
                    field=models.IntegerField(verbose_name='Stock Mínimo', help_text='Cantidad mínima requerida en inventario'),
                ),
            ],
        ),
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="ALTER TABLE inventario ADD COLUMN IF NOT EXISTS stock_maximo INTEGER NULL;",
                    reverse_sql="ALTER TABLE inventario DROP COLUMN IF EXISTS stock_maximo;",
                ),
            ],
            state_operations=[
                migrations.AddField(
                    model_name='inventario',
                    name='stock_maximo',
                    field=models.IntegerField(blank=True, null=True, verbose_name='Stock Máximo', help_text='Cantidad máxima permitida (opcional)'),
                ),
            ],
        ),
    ]
