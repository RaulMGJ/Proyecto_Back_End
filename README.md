# Lili's- Sistema de Gestión

## Descripción
Sistema de gestión completo para una dulcería desarrollado con Django, que incluye gestión de inventarios, productos, usuarios y roles con seguridad por permisos.

## Requisitos Cumplidos

###  **Todos los Requisitos Implementados:**

1. **✅ Conexión BD**: Configurado con .env y migraciones aplicadas sin error
2. **✅ Usuarios y roles**: 4 usuarios creados con permisos diferenciados
3. **✅ Admin Básico**: list_display, search_fields, list_filter, ordering, list_select_related
4. **✅ Admin Pro**: Inline, acción personalizada y validación implementadas
5. **✅ Seguridad**: Filtrado por rol y middleware de control de acceso

##  **GUÍA PASO A PASO - CONFIGURACIÓN MANUAL**

### **PASO 1: Preparar el Entorno**

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verificar que tienes XAMPP/WAMP/LAMP ejecutándose** con MySQL y phpMyAdmin

>  **Dependencias incluidas:**
> - Django 5.2.7 - Framework web principal
> - python-decouple 3.8 - Gestión de variables de entorno
> - mysqlclient 2.2.7 - Conector para MySQL
> - Herramientas adicionales para desarrollo

### **PASO 2: Configurar la Base de Datos en phpMyAdmin**

1. **Abrir phpMyAdmin:**
   - URL: http://localhost/phpmyadmin

2. **Crear la base de datos:**
   - Ve a la pestaña **"SQL"**
   - Copia y pega este código:

   ```sql
   CREATE DATABASE IF NOT EXISTS dulceria_db 
   CHARACTER SET utf8mb4 
   COLLATE utf8mb4_unicode_ci;
   
   USE dulceria_db;
   
   SHOW DATABASES LIKE 'dulceria_db';
   ```

3. **Hacer clic en "Continuar"**

### **PASO 3: Configurar el archivo .env**

1. **Abrir el archivo `.env`** en la raíz del proyecto

2. **Copiar exactamente este contenido:**

   ```
   SECRET_KEY=django-insecure-your-secret-key-here-change-in-production
   DEBUG=True
   USE_MYSQL=True
   DB_ENGINE=django.db.backends.mysql
   DB_NAME=dulceria_db
   DB_USER=root
   DB_PASSWORD=
   DB_HOST=localhost
   DB_PORT=3306
   ```

3. ** IMPORTANTE:** Si tu MySQL tiene contraseña, cambia `DB_PASSWORD=` por `DB_PASSWORD=tu_password`

### **PASO 4: Aplicar Migraciones**

1. **Ejecutar migraciones:**
   ```bash
   python manage.py migrate
   ```

2. **Cargar datos iniciales:**
   ```bash
   python manage.py loaddata fixtures/datos_iniciales.json
   ```

### **PASO 5: Iniciar el Servidor**

```bash
python manage.py runserver
```

### **PASO 6: Acceder al Sistema**

1. **Abrir navegador:** http://127.0.0.1:8000/admin/

2. **Usar credenciales del administrador:**
   - **Usuario:** `admin`
   - **Contraseña:** `admin123`

##  **Usuarios Disponibles**

### ** Credenciales de Acceso:**

| Rol | Usuario | Contraseña | Permisos |
|-----|---------|------------|----------|
| **Administrador** | `admin` | `admin123` | Acceso completo a todo |
| **Vendedor** | `vendedor1` | `vendedor123` | Solo lectura productos/inventarios |
| **Bodeguero** | `bodeguero1` | `bodeguero123` | Gestión productos e inventarios |
| **Cliente** | `cliente1` | `cliente123` | Bloqueado del admin |

##  **Estructura del Proyecto**

```
eva2backend/
├── dulceria_project/    # Configuración principal de Django
├── roles/              # Gestión de roles de usuario
├── usuarios/           # Modelo de usuario personalizado
├── productos/          # Catálogo de productos
├── inventarios/        # Control de inventario
├── fixtures/           # Datos iniciales
├── create_database.sql # Script SQL para phpMyAdmin
├── requirements.txt    # Dependencias del proyecto
├── manage.py          # Script de gestión de Django
└── README.md          # Esta guía
```

##  **Base de Datos**

### ** Tablas Creadas:**
- `rol` - Roles de usuario (Administrador, Vendedor, Bodeguero, Cliente)
- `usuario` - Usuarios del sistema con autenticación personalizada
- `producto` - Catálogo de productos de dulcería
- `inventario` - Control de stock por ubicación
- `django_migrations` - Control de migraciones
- `auth_*` - Tablas de autenticación de Django

### ** Datos Iniciales:**
- **4 roles** predefinidos
- **4 usuarios** de ejemplo
- **5 productos** de dulcería (chocolates, gomitas, caramelos, etc.)
- **7 registros** de inventario con diferentes ubicaciones

##  **Seguridad por Roles**

### ** Middleware de Control:**
- **Clientes**: Acceso completamente bloqueado al admin
- **Vendedores**: Solo productos e inventarios (lectura, solo stock > 0)
- **Bodegueros**: Productos e inventarios (lectura/escritura completa)
- **Administradores**: Acceso completo a todas las funcionalidades

### ** Permisos por Modelo:**
- **Productos**: Solo Administrador y Bodeguero pueden editar
- **Inventarios**: Vendedores ven solo stock > 0, Bodegueros ven todo
- **Roles**: Solo Administrador puede gestionar
- **Usuarios**: Solo Administrador puede gestionar

##  **Funcionalidades del Admin**

### ** Admin Básico:**
-  **list_display** configurado en todos los modelos
-  **search_fields** implementados para búsqueda rápida
-  **list_filter** aplicados para filtrado por categorías
-  **ordering** definido para ordenamiento lógico
-  **list_select_related** optimizado para consultas eficientes

### ** Admin Pro:**
-  **Inline**: InventarioInline en Productos (gestión integrada)
-  **Acción personalizada**: "Actualizar stock a 100 unidades" en Inventarios
-  **Validación**: Cantidad no puede ser negativa en Inventarios

##  **Consultas Útiles en phpMyAdmin**

### **Ver usuarios con sus roles:**
```sql
SELECT 
    u.username,
    u.nombre,
    u.correo,
    r.nombre as rol
FROM usuario u
JOIN rol r ON u.id_rol_id = r.id_rol;
```

### **Ver inventario con productos:**
```sql
SELECT 
    i.id_inventario,
    p.nombre as producto,
    i.cantidad_actual,
    i.ubicacion,
    i.fecha_ultima_actualizacion
FROM inventario i
JOIN producto p ON i.id_producto_id = p.id_producto
ORDER BY i.fecha_ultima_actualizacion DESC;
```

##  **Solución de Problemas**

### **Error: "Unknown database 'dulceria_db'"**
Ejecutar en phpMyAdmin:
```sql
CREATE DATABASE dulceria_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### **Error de conexión:**
1. Verificar que MySQL esté ejecutándose
2. Verificar credenciales en `.env`
3. Instalar mysqlclient: `pip install mysqlclient`

### **Error de permisos:**
```sql
GRANT ALL PRIVILEGES ON dulceria_db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

##  **Acceso al Sistema**

### ** URLs Importantes:**
- **phpMyAdmin**: http://localhost/phpmyadmin
- **Admin Django**: http://127.0.0.1:8000/admin/
- **Base de datos**: `dulceria_db`

### ** Usuarios de Prueba:**
- **admin** / admin123 (Administrador completo)
- **vendedor1** / vendedor123 (Solo lectura)
- **bodeguero1** / bodeguero123 (Gestión inventarios)
- **cliente1** / cliente123 (Bloqueado)

##  **Próximos Pasos**

1. **✅ Explorar phpMyAdmin** y familiarizarse con las tablas
2. **✅ Probar diferentes usuarios** en el admin de Django
3. **✅ Verificar permisos** por rol
4. **✅ Crear datos adicionales** si es necesario
5. **✅ Configurar respaldos** automáticos

##  **Notas Técnicas**

- Modelo de usuario personalizado con campo `correo` como USERNAME_FIELD
- Validaciones en modelo Inventario (cantidad >= 0)
- Middleware personalizado para control de acceso
- Configuración bilingüe (español/inglés)
- Timezone configurado para Colombia

¡Tu sistema está listo para usar con phpMyAdmin! 🎉
