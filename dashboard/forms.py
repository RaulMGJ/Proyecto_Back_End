from django import forms
from productos.models import Producto
from inventarios.models import Inventario

class ProductoForm(forms.ModelForm):
    """Formulario para crear/editar productos"""
    
    # Campos adicionales para validaciones F-PROD-VAL-04
    UNIDADES_CHOICES = [
        ('', 'Seleccione...'),
        ('Unidad', 'Unidad'),
        ('Caja', 'Caja'),
        ('Paquete', 'Paquete'),
        ('Docena', 'Docena'),
        ('Kilogramo', 'Kilogramo'),
        ('Litro', 'Litro'),
    ]
    
    unidad_compra = forms.ChoiceField(
        choices=UNIDADES_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Unidad de Compra'
    )
    
    unidad_venta = forms.ChoiceField(
        choices=UNIDADES_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Unidad de Venta'
    )
    
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
                'class': 'form-select'
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
        """Evitar precios negativos o cero en el formulario."""
        precio = self.cleaned_data.get('precio_referencia')
        if precio is None:
            raise forms.ValidationError('El precio es obligatorio')
        if precio < 0:
            raise forms.ValidationError('El precio no puede ser negativo')
        return precio
    
    def clean_unidad_compra(self):
        """F-PROD-VAL-04: Validar que unidad_compra no esté vacía"""
        unidad = self.cleaned_data.get('unidad_compra')
        if not unidad:
            raise forms.ValidationError('La unidad de compra es obligatoria')
        return unidad
    
    def clean_unidad_venta(self):
        """F-PROD-VAL-04: Validar que unidad_venta no esté vacía"""
        unidad = self.cleaned_data.get('unidad_venta')
        if not unidad:
            raise forms.ValidationError('La unidad de venta es obligatoria')
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

    def clean_cantidad_actual(self):
        cantidad = self.cleaned_data.get('cantidad_actual')
        if cantidad is None:
            raise forms.ValidationError('La cantidad actual es obligatoria')
        if cantidad < 0:
            raise forms.ValidationError('La cantidad actual no puede ser negativa')
        return cantidad
    
    def clean_stock_minimo(self):
        """F-PROD-VAL-05: Validar que stock_minimo no esté vacío"""
        stock_min = self.cleaned_data.get('stock_minimo')
        if stock_min is None:
            raise forms.ValidationError('El stock mínimo es obligatorio')
        if stock_min < 0:
            raise forms.ValidationError('El stock mínimo no puede ser negativo')
        return stock_min

    def clean_stock_maximo(self):
        stock_max = self.cleaned_data.get('stock_maximo')
        if stock_max is not None and stock_max < 0:
            raise forms.ValidationError('El stock máximo no puede ser negativo')
        return stock_max
    
    def clean(self):
        cleaned_data = super().clean()
        stock_min = cleaned_data.get('stock_minimo')
        stock_max = cleaned_data.get('stock_maximo')
        
        if stock_max is not None and stock_min is not None:
            if stock_max < stock_min:
                raise forms.ValidationError('El stock máximo no puede ser menor que el stock mínimo')
        
        return cleaned_data
