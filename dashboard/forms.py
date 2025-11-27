from django import forms
from productos.models import Producto
from inventarios.models import Inventario

class ProductoForm(forms.ModelForm):
    """Formulario para crear/editar productos"""
    
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio_referencia', 'unidad_medida']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej: Chocolatina Jet'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Descripción del producto',
                'rows': 3
            }),
            'precio_referencia': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Precio en pesos chilenos',
                'min': '0',
                'step': '100'
            }),
            'unidad_medida': forms.Select(attrs={
                'class': 'form-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].label = 'Nombre del Producto'
        self.fields['descripcion'].label = 'Descripción'
        self.fields['descripcion'].required = False
        self.fields['precio_referencia'].label = 'Precio de Venta'
        self.fields['unidad_medida'].label = 'Unidad de Medida'
    
    def clean_precio_referencia(self):
        precio = self.cleaned_data.get('precio_referencia')
        if precio is not None and precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a 0')
        return precio
    
    def clean_unidad_medida(self):
        """F-PROD-VAL-04: Validar que unidad_medida no esté vacía"""
        unidad = self.cleaned_data.get('unidad_medida')
        if not unidad:
            raise forms.ValidationError('La unidad de medida es obligatoria')
        return unidad

class InventarioForm(forms.ModelForm):
    """Formulario para crear/editar inventarios"""
    
    class Meta:
        model = Inventario
        fields = ['id_producto', 'cantidad_actual', 'stock_minimo', 'stock_maximo', 'ubicacion']
        widgets = {
            'id_producto': forms.Select(attrs={
                'class': 'form-input'
            }),
            'cantidad_actual': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Cantidad en stock',
                'min': '0'
            }),
            'stock_minimo': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Cantidad mínima requerida',
                'min': '0'
            }),
            'stock_maximo': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Cantidad máxima (opcional)',
                'min': '0'
            }),
            'ubicacion': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej: Estante A1, Bodega Principal'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_producto'].label = 'Producto'
        self.fields['cantidad_actual'].label = 'Cantidad Actual'
        self.fields['stock_minimo'].label = 'Stock Mínimo'
        self.fields['stock_maximo'].label = 'Stock Máximo (opcional)'
        self.fields['stock_maximo'].required = False
        self.fields['ubicacion'].label = 'Ubicación'
        
        # Filtrar productos que ya tienen inventario
        if self.instance.pk is None:  # Solo para nuevos inventarios
            productos_con_inventario = Inventario.objects.values_list('id_producto', flat=True)
            self.fields['id_producto'].queryset = Producto.objects.exclude(
                id_producto__in=productos_con_inventario
            )
    
    def clean_stock_minimo(self):
        """F-PROD-VAL-05: Validar que stock_minimo no esté vacío"""
        stock_min = self.cleaned_data.get('stock_minimo')
        if stock_min is None:
            raise forms.ValidationError('El stock mínimo es obligatorio')
        if stock_min < 0:
            raise forms.ValidationError('El stock mínimo no puede ser negativo')
        return stock_min
    
    def clean(self):
        cleaned_data = super().clean()
        stock_min = cleaned_data.get('stock_minimo')
        stock_max = cleaned_data.get('stock_maximo')
        
        if stock_max is not None and stock_min is not None:
            if stock_max < stock_min:
                raise forms.ValidationError('El stock máximo no puede ser menor que el stock mínimo')
        
        return cleaned_data
