# Generated manually to add stock_minimo y stock_maximo a inventario
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventarios', '0002_movimientoinventario'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME='inventario' AND COLUMN_NAME='stock_minimo' 
                INTO @stock_minimo_exists;
                SET @sql = IF(@stock_minimo_exists IS NULL, 
                    'ALTER TABLE inventario ADD COLUMN stock_minimo INTEGER NOT NULL DEFAULT 0', 
                    'SELECT 1');
                PREPARE stmt FROM @sql;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
            """,
            reverse_sql="ALTER TABLE inventario DROP COLUMN IF EXISTS stock_minimo;",
            state_operations=[
                migrations.AddField(
                    model_name='inventario',
                    name='stock_minimo',
                    field=models.IntegerField(verbose_name='Stock Mínimo', help_text='Cantidad mínima requerida en inventario'),
                ),
            ]
        ),
        migrations.RunSQL(
            sql="""
                SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME='inventario' AND COLUMN_NAME='stock_maximo' 
                INTO @stock_maximo_exists;
                SET @sql = IF(@stock_maximo_exists IS NULL, 
                    'ALTER TABLE inventario ADD COLUMN stock_maximo INTEGER NULL', 
                    'SELECT 1');
                PREPARE stmt FROM @sql;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
            """,
            reverse_sql="ALTER TABLE inventario DROP COLUMN IF EXISTS stock_maximo;",
            state_operations=[
                migrations.AddField(
                    model_name='inventario',
                    name='stock_maximo',
                    field=models.IntegerField(blank=True, null=True, verbose_name='Stock Máximo', help_text='Cantidad máxima permitida (opcional)'),
                ),
            ]
        ),
    ]
