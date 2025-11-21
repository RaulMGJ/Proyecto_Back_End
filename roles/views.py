from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Rol


@login_required
def lista_roles(request):
    """Vista para listar todos los roles"""
    user = request.user
    
    # Solo administradores pueden gestionar roles
    if not (user.is_superuser or (hasattr(user, 'id_rol') and user.id_rol.nombre == 'Administrador')):
        messages.error(request, 'No tienes permisos para gestionar roles')
        return redirect('dashboard:home')
    
    roles = Rol.objects.all().order_by('id_rol')
    
    context = {
        'roles': roles,
        'user': user,
    }
    return render(request, 'dashboard/roles.html', context)


@login_required
def crear_rol(request):
    """Vista para crear un nuevo rol"""
    user = request.user
    
    if not (user.is_superuser or (hasattr(user, 'id_rol') and user.id_rol.nombre == 'Administrador')):
        return JsonResponse({'success': False, 'message': 'No tienes permisos'}, status=403)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        
        if not nombre:
            return JsonResponse({'success': False, 'message': 'El nombre es requerido'})
        
        # Verificar que no exista
        if Rol.objects.filter(nombre=nombre).exists():
            return JsonResponse({'success': False, 'message': 'Ya existe un rol con ese nombre'})
        
        # Crear rol
        rol = Rol.objects.create(nombre=nombre, descripcion=descripcion)
        
        return JsonResponse({
            'success': True,
            'message': f'Rol "{nombre}" creado exitosamente',
            'rol': {
                'id': rol.id_rol,
                'nombre': rol.nombre,
                'descripcion': rol.descripcion
            }
        })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)


@login_required
def editar_rol(request, rol_id):
    """Vista para editar un rol"""
    user = request.user
    
    if not (user.is_superuser or (hasattr(user, 'id_rol') and user.id_rol.nombre == 'Administrador')):
        return JsonResponse({'success': False, 'message': 'No tienes permisos'}, status=403)
    
    rol = get_object_or_404(Rol, pk=rol_id)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        
        if not nombre:
            return JsonResponse({'success': False, 'message': 'El nombre es requerido'})
        
        # Verificar que no exista otro rol con ese nombre
        if Rol.objects.filter(nombre=nombre).exclude(id_rol=rol_id).exists():
            return JsonResponse({'success': False, 'message': 'Ya existe un rol con ese nombre'})
        
        # Actualizar rol
        rol.nombre = nombre
        rol.descripcion = descripcion
        rol.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Rol "{nombre}" actualizado exitosamente'
        })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)


@login_required
def eliminar_rol(request, rol_id):
    """Vista para eliminar un rol"""
    user = request.user
    
    if not (user.is_superuser or (hasattr(user, 'id_rol') and user.id_rol.nombre == 'Administrador')):
        return JsonResponse({'success': False, 'message': 'No tienes permisos'}, status=403)
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)
    
    rol = get_object_or_404(Rol, pk=rol_id)
    
    # Verificar si hay usuarios con este rol
    usuarios_count = rol.usuario_set.count()
    if usuarios_count > 0:
        return JsonResponse({
            'success': False,
            'message': f'No se puede eliminar. Hay {usuarios_count} usuario(s) con este rol'
        })
    
    nombre = rol.nombre
    rol.delete()
    
    return JsonResponse({
        'success': True,
        'message': f'Rol "{nombre}" eliminado exitosamente'
    })
