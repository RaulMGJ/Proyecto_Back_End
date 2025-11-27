from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
import uuid
from roles.models import Rol

class Usuario(AbstractUser):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150, verbose_name="Nombre")
    correo = models.EmailField(max_length=191, unique=True, verbose_name="Correo Electrónico")
    contrasena = models.CharField(max_length=128, verbose_name="Contraseña")
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE, verbose_name="Rol")
    
    # Campos de perfil
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Avatar")
    
    # Campos de seguridad anti-fuerza bruta
    failed_login_attempts = models.IntegerField(default=0, verbose_name="Intentos fallidos de login")
    locked_until = models.DateTimeField(null=True, blank=True, verbose_name="Bloqueado hasta")
    
    # Campos adicionales para AbstractUser
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['correo', 'nombre']
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = "usuario"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.id_rol.nombre})"
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.correo
        if not self.email:
            self.email = self.correo
        super().save(*args, **kwargs)
    
    def is_account_locked(self):
        """Verifica si la cuenta está bloqueada por intentos fallidos"""
        if self.locked_until and timezone.now() < self.locked_until:
            return True
        return False
    
    def reset_failed_attempts(self):
        """Resetea el contador de intentos fallidos"""
        self.failed_login_attempts = 0
        self.locked_until = None
        self.save(update_fields=['failed_login_attempts', 'locked_until'])
    
    def increment_failed_attempts(self):
        """Incrementa el contador de intentos fallidos y bloquea si es necesario"""
        self.failed_login_attempts += 1
        
        # Bloquear cuenta después de 5 intentos fallidos por 30 minutos
        if self.failed_login_attempts >= 5:
            self.locked_until = timezone.now() + timedelta(minutes=30)
        
        self.save(update_fields=['failed_login_attempts', 'locked_until'])


class PasswordResetToken(models.Model):
    """Modelo para almacenar tokens de recuperación de contraseña"""
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Token de Recuperación"
        verbose_name_plural = "Tokens de Recuperación"
        db_table = "password_reset_token"
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            # Token válido por 5 minutos
            self.expires_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)
    
    def is_valid(self):
        """Verifica si el token es válido"""
        return not self.is_used and timezone.now() < self.expires_at
    
    def __str__(self):
        return f"Token para {self.usuario.correo} - {'Válido' if self.is_valid() else 'Expirado/Usado'}"
