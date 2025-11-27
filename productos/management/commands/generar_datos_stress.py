from django.core.management.base import BaseCommand
from productos.models import Producto
from inventarios.models import Inventario
from django.utils import timezone
import random

class Command(BaseCommand):
    help = "Genera entre 5,000 y 10,000 registros para pruebas de stress/rendimiento"

    def add_arguments(self, parser):
        parser.add_argument('--productos', type=int, default=5000, help='Cantidad de productos a crear')
        parser.add_argument('--inventarios-por-producto', type=int, default=2, help='Inventarios por producto (promedio)')
        parser.add_argument('--limpiar', action='store_true', help='Eliminar datos existentes antes de generar')

    def handle(self, *args, **options):
        num_productos = options['productos']
        inventarios_por_producto = options['inventarios_por_producto']
        limpiar = options['limpiar']

        if limpiar:
            self.stdout.write(self.style.WARNING('Limpiando datos existentes...'))
            Inventario.objects.all().delete()
            Producto.objects.all().delete()
            self.stdout.write('Datos eliminados.')

        self.stdout.write(f'Generando {num_productos} productos...')
        
        # Categorías de productos para dulcería
        categorias = [
            'Alfajor', 'Trufa', 'Bombón', 'Caramelo', 'Gomita',
            'Chocolate', 'Piruleta', 'Chicle', 'Mazapán', 'Turrón',
            'Brownie', 'Cookie', 'Galletita', 'Wafer', 'Oblea'
        ]
        
        sabores = [
            'Chocolate', 'Vainilla', 'Fresa', 'Limón', 'Naranja',
            'Menta', 'Café', 'Caramelo', 'Coco', 'Frambuesa',
            'Dulce de Leche', 'Maracuyá', 'Cereza', 'Pistacho', 'Avellana',
            'Almendra', 'Nuez', 'Miel', 'Canela', 'Jengibre'
        ]
        
        ubicaciones = [
            'Estante A1', 'Estante A2', 'Estante A3', 'Estante A4',
            'Estante B1', 'Estante B2', 'Estante B3', 'Estante B4',
            'Estante C1', 'Estante C2', 'Estante C3', 'Estante C4',
            'Bodega Principal', 'Bodega Secundaria', 'Almacén Norte',
            'Almacén Sur', 'Depósito 1', 'Depósito 2', 'Refrigerador A', 'Refrigerador B'
        ]

        productos_creados = []
        batch_size = 1000
        
        for i in range(num_productos):
            categoria = random.choice(categorias)
            sabor = random.choice(sabores)
            numero = random.randint(1, 9999)
            
            producto = Producto(
                nombre=f"{categoria} de {sabor} #{numero}",
                descripcion=f"{categoria} artesanal sabor {sabor} - Lote {numero}",
                precio_referencia=random.randint(1500, 8000)
            )
            productos_creados.append(producto)
            
            # Crear en lotes para eficiencia
            if len(productos_creados) >= batch_size:
                Producto.objects.bulk_create(productos_creados, ignore_conflicts=True)
                self.stdout.write(f'  → {i + 1} productos creados...')
                productos_creados = []
        
        # Crear productos restantes
        if productos_creados:
            Producto.objects.bulk_create(productos_creados, ignore_conflicts=True)
        
        self.stdout.write(self.style.SUCCESS(f'✓ {num_productos} productos creados'))
        
        # Generar inventarios
        self.stdout.write(f'Generando inventarios (~{num_productos * inventarios_por_producto})...')
        
        productos = Producto.objects.all()
        inventarios_creados = []
        total_inventarios = 0
        
        for producto in productos:
            # Crear entre 1 y 3 inventarios por producto
            num_inv = random.randint(1, inventarios_por_producto + 1)
            
            for _ in range(num_inv):
                inventario = Inventario(
                    id_producto=producto,
                    cantidad_actual=random.randint(0, 500),
                    ubicacion=random.choice(ubicaciones),
                    fecha_ultima_actualizacion=timezone.now()
                )
                inventarios_creados.append(inventario)
                total_inventarios += 1
                
                # Crear en lotes
                if len(inventarios_creados) >= batch_size:
                    Inventario.objects.bulk_create(inventarios_creados, ignore_conflicts=True)
                    self.stdout.write(f'  → {total_inventarios} inventarios creados...')
                    inventarios_creados = []
        
        # Crear inventarios restantes
        if inventarios_creados:
            Inventario.objects.bulk_create(inventarios_creados, ignore_conflicts=True)
        
        self.stdout.write(self.style.SUCCESS(f'✓ {total_inventarios} inventarios creados'))
        
        # Resumen
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('═══════════════════════════════════'))
        self.stdout.write(self.style.SUCCESS('  DATOS DE STRESS GENERADOS'))
        self.stdout.write(self.style.SUCCESS('═══════════════════════════════════'))
        self.stdout.write(f'Total Productos:   {Producto.objects.count():,}')
        self.stdout.write(f'Total Inventarios: {Inventario.objects.count():,}')
        self.stdout.write(self.style.SUCCESS('═══════════════════════════════════'))
        self.stdout.write('')
        self.stdout.write('Listo para pruebas de:')
        self.stdout.write('  • Paginación con miles de registros')
        self.stdout.write('  • Filtros y búsqueda en volumen')
        self.stdout.write('  • Ordenamiento de grandes conjuntos')
        self.stdout.write('  • Rendimiento de queries con JOIN')
