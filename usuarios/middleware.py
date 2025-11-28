from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.shortcuts import redirect

User = get_user_model()

class RolMiddleware:
    """Control de acceso al admin basado en roles."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            if request.path in ['/admin/', '/admin/login/', '/admin/logout/']:
                return self.get_response(request)
            if request.user.is_authenticated:
                user_role = getattr(getattr(request.user, 'id_rol', None), 'nombre', None)
                if user_role == 'Cliente':
                    return HttpResponseForbidden("No tienes permisos para acceder a esta sección.")
                elif user_role in ['Vendedor', 'Bodeguero']:
                    allowed_paths = ['/admin/productos/', '/admin/inventarios/', '/admin/']
                    if not any(request.path.startswith(path) for path in allowed_paths):
                        return HttpResponseForbidden("No tienes permisos para acceder a esta sección.")
        return self.get_response(request)


class ForcePasswordChangeMiddleware:
    """Bloquea toda navegación hasta que el usuario cambie su contraseña temporal.

    Cumple requisito F-FIRST-LOGIN-02: no permitir acceso a otras pantallas
    mientras `debe_cambiar_clave` esté activo. También soporta peticiones AJAX
    devolviendo JSON para que el frontend pueda redirigir limpiamente.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        if user and user.is_authenticated and getattr(user, 'debe_cambiar_clave', False):
            path = request.path
            # Rutas permitidas mientras cambia la contraseña
            allowed_prefixes = [
                '/reset-password',
                '/dashboard/reset-password',
                '/login',
                '/logout',
                '/static/',
                '/forgot-password',
                '/admin/logout/',  # permitir salir si está en admin
            ]
            if not any(path.startswith(pref) for pref in allowed_prefixes):
                # Respuesta especial para AJAX
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    from django.http import JsonResponse
                    from django.urls import reverse
                    return JsonResponse({
                        'success': False,
                        'must_change_password': True,
                        'redirect': reverse('reset_password'),
                        'message': 'Debes cambiar tu contraseña antes de continuar.'
                    }, status=403)
                from django.urls import reverse
                return redirect(reverse('reset_password'))
        return self.get_response(request)
