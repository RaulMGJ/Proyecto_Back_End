"""
Comando de gestión para limpiar tokens de recuperación expirados
Uso: python manage.py cleanup_expired_tokens
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from usuarios.models import PasswordResetToken


class Command(BaseCommand):
    help = 'Elimina tokens de recuperación de contraseña expirados o usados'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Eliminar tokens con más de X días (por defecto 7)'
        )

    def handle(self, *args, **options):
        days = options['days']
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        
        # Tokens expirados
        expired_tokens = PasswordResetToken.objects.filter(
            expires_at__lt=timezone.now()
        )
        
        # Tokens usados y antiguos
        old_used_tokens = PasswordResetToken.objects.filter(
            is_used=True,
            created_at__lt=cutoff_date
        )
        
        # Contar antes de eliminar
        expired_count = expired_tokens.count()
        used_count = old_used_tokens.count()
        total_count = expired_count + used_count
        
        # Eliminar
        expired_tokens.delete()
        old_used_tokens.delete()
        
        # Mensaje de éxito
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Limpieza completada:'
            )
        )
        self.stdout.write(f'   - Tokens expirados eliminados: {expired_count}')
        self.stdout.write(f'   - Tokens usados antiguos eliminados: {used_count}')
        self.stdout.write(f'   - Total: {total_count} tokens eliminados')
        
        # Mostrar estadísticas actuales
        active_tokens = PasswordResetToken.objects.filter(
            is_used=False,
            expires_at__gt=timezone.now()
        ).count()
        
        self.stdout.write(f'\n📊 Estadísticas actuales:')
        self.stdout.write(f'   - Tokens activos: {active_tokens}')
        self.stdout.write(f'   - Total en BD: {PasswordResetToken.objects.count()}')
