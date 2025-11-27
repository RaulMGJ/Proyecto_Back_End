from django.core.management.base import BaseCommand
from django.db import transaction
from proveedores.models import Proveedor
import random
import string


def calcular_dv_rut(cuerpo: int) -> str:
    """Calcula el dígito verificador de un RUT chileno dado el cuerpo numérico."""
    factors = [2, 3, 4, 5, 6, 7]
    total = 0
    factor_idx = 0
    for d in map(int, reversed(str(cuerpo))):
        total += d * factors[factor_idx]
        factor_idx = (factor_idx + 1) % len(factors)
    remainder = 11 - (total % 11)
    if remainder == 11:
        return '0'
    if remainder == 10:
        return 'K'
    return str(remainder)


def generar_rut_unico(existentes: set) -> str:
    """Genera un RUT válido y único no presente en 'existentes'."""
    while True:
        cuerpo = random.randint(10_000_000, 27_000_000)  # rango razonable
        dv = calcular_dv_rut(cuerpo)
        rut = f"{cuerpo}-{dv}"
        if rut not in existentes:
            existentes.add(rut)
            return rut


def nombre_ficticio(i: int) -> str:
    prefijos = ["Comercial", "Distribuidora", "Importadora", "Confites", "Dulces", "Alimentos"]
    sufijos = ["Andes", "Pacífico", "Austral", "Central", "Del Norte", "Del Sur", "Premium"]
    return f"{random.choice(prefijos)} {random.choice(sufijos)} #{i:04d}"


def contacto_ficticio() -> str:
    nombres = ["Juan", "María", "Pedro", "Lucía", "Carlos", "Ana", "Sofía", "Tomás", "Daniela", "Felipe"]
    apellidos = ["Pérez", "González", "Silva", "Rojas", "Torres", "Castro", "Vargas", "Flores", "Suárez", "López"]
    return f"{random.choice(nombres)} {random.choice(apellidos)}"


def direccion_ficticia() -> str:
    calles = ["Av. Libertador", "Calle Principal", "Av. Los Héroes", "Calle 21 de Mayo", "Pasaje Central", "Camino Real"]
    numero = random.randint(10, 9999)
    comuna = random.choice(["Santiago", "Providencia", "Ñuñoa", "Maipú", "Las Condes", "La Florida"])
    return f"{random.choice(calles)} {numero}, {comuna}"


class Command(BaseCommand):
    help = "Genera proveedores de prueba en masa para pruebas de estrés (por defecto 5000)"

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=5000, help='Cantidad de proveedores a crear')
        parser.add_argument('--batch', type=int, default=1000, help='Tamaño de lote para bulk_create')
        parser.add_argument('--truncate', action='store_true', help='Borra todos los proveedores antes de generar')

    def handle(self, *args, **options):
        count = options['count']
        batch_size = options['batch']
        truncate = options['truncate']

        if truncate:
            self.stdout.write(self.style.WARNING('Eliminando proveedores existentes...'))
            Proveedor.objects.all().delete()

        existentes = set(Proveedor.objects.values_list('rut_nif', flat=True))
        to_create = []

        self.stdout.write(self.style.SUCCESS(f'Generando {count} proveedores en lotes de {batch_size}...'))
        for i in range(1, count + 1):
            rut = generar_rut_unico(existentes)
            nombre = nombre_ficticio(i)
            contacto = contacto_ficticio()
            direccion = direccion_ficticia()
            email_local = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            email = f"{email_local}@example.test"

            prov = Proveedor(
                rut_nif=rut,
                nombre=nombre,
                contacto=contacto,
                direccion=direccion,
                pais='Chile',
                email=email,
                email_secundario=None,
            )
            to_create.append(prov)

            if len(to_create) >= batch_size:
                Proveedor.objects.bulk_create(to_create, batch_size=batch_size)
                to_create.clear()
                if i % batch_size == 0:
                    self.stdout.write(f"  -> {i} proveedores creados...")

        if to_create:
            Proveedor.objects.bulk_create(to_create, batch_size=batch_size)

        total = Proveedor.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Listo. Total de proveedores: {total}'))
