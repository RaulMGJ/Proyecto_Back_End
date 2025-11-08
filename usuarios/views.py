from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from .models import Usuario
from roles.models import Rol
from django import forms

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Contraseña'}),
        label='Contraseña'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirmar contraseña'}),
        label='Confirmar contraseña'
    )
    
    class Meta:
        model = Usuario
        fields = ['nombre', 'correo', 'id_rol', 'is_active']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nombre completo'}),
            'correo': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'correo@ejemplo.com'}),
            'id_rol': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
        
    def __init__(self, *args, **kwargs):
        self.is_edit = kwargs.pop('is_edit', False)
        super().__init__(*args, **kwargs)
        
        if self.is_edit:
            self.fields['password'].required = False
            self.fields['confirm_password'].required = False
            self.fields['password'].help_text = "Deja en blanco para mantener la contraseña actual"
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if not self.is_edit or password:
            if password != confirm_password:
                raise forms.ValidationError("Las contraseñas no coinciden")
                
        return cleaned_data

@login_required
@staff_member_required
def lista_usuarios(request):
    """Vista para listar todos los usuarios"""
    usuarios = Usuario.objects.select_related('id_rol').all().order_by('-date_joined')
    
    # Búsqueda
    search = request.GET.get('search', '')
    if search:
        usuarios = usuarios.filter(nombre__icontains=search) | usuarios.filter(correo__icontains=search)
    
    # Paginación
    paginator = Paginator(usuarios, 10)
    page = request.GET.get('page')
    usuarios = paginator.get_page(page)
    
    context = {
        'usuarios': usuarios,
        'search': search,
        'total_usuarios': Usuario.objects.count(),
        'usuarios_activos': Usuario.objects.filter(is_active=True).count(),
    }
    return render(request, 'dashboard/usuarios.html', context)

@login_required
@staff_member_required
def agregar_usuario(request):
    """Vista para agregar un nuevo usuario"""
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            # Establecer username como correo
            usuario.username = form.cleaned_data['correo']
            usuario.email = form.cleaned_data['correo']
            # Encriptar contraseña
            usuario.password = make_password(form.cleaned_data['password'])
            usuario.save()
            
            # Si es una petición AJAX, responder con JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
                from django.http import JsonResponse
                return JsonResponse({
                    'success': True,
                    'user': {
                        'id': usuario.id_usuario,
                        'nombre': usuario.nombre,
                        'correo': usuario.correo,
                        'rol': usuario.id_rol.nombre,
                        'is_active': usuario.is_active
                    }
                })
            
            messages.success(request, f'Usuario "{usuario.nombre}" creado exitosamente.')
            return redirect('usuarios:lista_usuarios')
        else:
            # Si hay errores y es AJAX, responder con JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
                from django.http import JsonResponse
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
    else:
        form = UsuarioForm()
    
    # Obtener todos los usuarios para mostrar en la lista
    usuarios = Usuario.objects.select_related('id_rol').all().order_by('-date_joined')
    
    context = {
        'form': form,
        'usuarios': usuarios,
        'title': 'Agregar Usuario',
        'action': 'agregar'
    }
    return render(request, 'dashboard/form_usuario.html', context)

@login_required
@staff_member_required
def editar_usuario(request, usuario_id):
    """Vista para editar un usuario existente"""
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario, is_edit=True)
        if form.is_valid():
            usuario = form.save(commit=False)
            # Actualizar contraseña solo si se proporcionó una nueva
            if form.cleaned_data['password']:
                usuario.password = make_password(form.cleaned_data['password'])
            usuario.save()
            
            messages.success(request, f'Usuario "{usuario.nombre}" actualizado exitosamente.')
            return redirect('usuarios:lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario, is_edit=True)
    
    context = {
        'form': form,
        'usuario': usuario,
        'title': 'Editar Usuario',
        'action': 'editar'
    }
    return render(request, 'dashboard/form_usuario.html', context)

@login_required
@staff_member_required
def eliminar_usuario(request, usuario_id):
    """Vista para eliminar un usuario"""
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    
    if request.method == 'POST':
        nombre = usuario.nombre
        usuario.delete()
        messages.success(request, f'Usuario "{nombre}" eliminado exitosamente.')
        return redirect('usuarios:lista_usuarios')
    
    # Si es una petición GET desde el modal, redirigir a la lista
    # ya que el modal se maneja en el frontend
    return redirect('usuarios:lista_usuarios')

@login_required
@staff_member_required
def toggle_usuario_status(request, usuario_id):
    """Vista para activar/desactivar usuario"""
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    usuario.is_active = not usuario.is_active
    usuario.save()
    
    status = "activado" if usuario.is_active else "desactivado"
    messages.success(request, f'Usuario "{usuario.nombre}" {status} exitosamente.')
    return redirect('usuarios:lista_usuarios')
