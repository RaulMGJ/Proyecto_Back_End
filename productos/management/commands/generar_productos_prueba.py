from django.core.management.base import BaseCommand
from productos.models import Producto
import random


class Command(BaseCommand):
    help = 'Genera productos ficticios para pruebas de stress y rendimiento'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cantidad',
            type=int,
            default=10000,
            help='Cantidad de productos a generar (por defecto: 10000)'
        )

    def handle(self, *args, **options):
        cantidad = options['cantidad']
        
        self.stdout.write(self.style.WARNING(f'Generando {cantidad} productos de prueba...'))
        
        # Listas para nombres y descripciones realistas
        prefijos = ['Chocolate', 'Caramelo', 'Dulce', 'Gomita', 'Chicle', 'Paleta', 'Galleta', 
                    'Pirulí', 'Bombón', 'Toffee', 'Malvavisco', 'Gragea', 'Regaliz', 'Mentita']
        
        sufijos = ['Premium', 'Deluxe', 'Clásico', 'Extra', 'Light', 'Mega', 'Mini', 'Suave',
                   'Intenso', 'Tropical', 'Frutilla', 'Menta', 'Vainilla', 'Coco', 'Naranja']
        
        sabores = ['fresa', 'limón', 'naranja', 'uva', 'manzana', 'cereza', 'piña', 'sandía',
                   'durazno', 'mora', 'frambuesa', 'mango', 'maracuyá', 'coco', 'vainilla']
        
        # Generar productos en lotes para mejor rendimiento
        batch_size = 1000
        productos = []
        
        for i in range(cantidad):
            nombre = f"{random.choice(prefijos)} {random.choice(sufijos)} {i+1}"
            sabor = random.choice(sabores)
            descripcion = f"Delicioso dulce sabor a {sabor}, ideal para compartir o disfrutar solo"
            precio = random.randint(50, 5000)  # Precios entre 50 y 5000 pesos
            
            productos.append(Producto(
                nombre=nombre,
                descripcion=descripcion,
                precio_referencia=precio
            ))
            
            # Insertar en lotes
            if len(productos) >= batch_size:
                Producto.objects.bulk_create(productos, ignore_conflicts=True)
                self.stdout.write(self.style.SUCCESS(f'✓ {i+1} productos creados...'))
                productos = []
        
        # Insertar los productos restantes
        if productos:
            Producto.objects.bulk_create(productos, ignore_conflicts=True)
        
        total = Producto.objects.count()
        self.stdout.write(self.style.SUCCESS(f'✅ Proceso completado. Total de productos en BD: {total}'))
