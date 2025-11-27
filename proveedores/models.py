from django.db import models
from django.core.exceptions import ValidationError


def validar_rut_chileno(rut: str):
    """
    Valida RUT chileno en formato sin puntos y con guion: 12345678-5 o 1234567-K
    - Limpia espacios
    - Verifica dígito verificador
    """
    if not rut:
        raise ValidationError("El RUT es obligatorio")

    rut = rut.strip().upper()
    # Permitir solo formato con guion
    if '-' not in rut:
        raise ValidationError("Formato de RUT inválido. Usa 12345678-5")

    cuerpo, dv = rut.split('-', 1)
    if not cuerpo.isdigit():
        raise ValidationError("El cuerpo del RUT debe ser numérico")

    # Calcular dígito verificador
    reversed_digits = map(int, reversed(cuerpo))
    factors = [2, 3, 4, 5, 6, 7]
    total = 0
    factor_idx = 0
    for d in reversed_digits:
        total += d * factors[factor_idx]
        factor_idx = (factor_idx + 1) % len(factors)
    remainder = 11 - (total % 11)
    dv_calc = '0' if remainder == 11 else 'K' if remainder == 10 else str(remainder)

    if dv_calc != dv:
        raise ValidationError("RUT inválido (dígito verificador no coincide)")

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    contacto = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    rut_nif = models.CharField(
        max_length=12,
        unique=True,
        verbose_name="RUT",
        help_text="Formato: 12345678-5 (sin puntos)",
        blank=False,
        validators=[validar_rut_chileno]
    )
    email = models.EmailField(
        verbose_name="Email",
        help_text="Email principal (obligatorio)",
        blank=False,
        default="no-email@example.invalid"
    )
    email_secundario = models.EmailField(
        verbose_name="Email Secundario",
        help_text="Email alternativo (opcional)",
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'proveedor'
