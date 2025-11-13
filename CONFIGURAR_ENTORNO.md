# 🔧 Configurar Entorno en Universidad

## 📋 Pasos para configurar el proyecto en cualquier PC:

### 1. **Clonar el repositorio:**
```bash
git clone https://github.com/RaulMGJ/Proyecto_Back_End.git
cd prueba
```

### 2. **Copiar el archivo de configuración:**
```bash
# En Windows (el archivo .env.example ya tiene el punto al inicio)
copy .env.example .env

# En Linux/Mac
cp .env.example .env
```

**Nota:** El archivo `.env.example` ya tiene el punto al inicio, por lo que Windows lo reconocerá como archivo de configuración y le mostrará el ícono de la tuerca 🔧.

### 3. **Editar el archivo .env:**
Abrir el archivo `.env` y cambiar solo los valores que necesites:

```env
SECRET_KEY=tu-secret-key-aqui-cambiar-en-produccion
DEBUG=True
USE_MYSQL=True
DB_ENGINE=django.db.backends.mysql
DB_NAME=dulceria_db
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
```

**Cambios típicos:**
- `SECRET_KEY`: Generar una nueva clave secreta
- `DB_PASSWORD`: Agregar contraseña si MySQL la tiene
- `DB_USER`: Cambiar si no es 'root'
- `DB_HOST`: Cambiar si MySQL está en otro servidor

### 4. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

### 5. **Configurar base de datos:**
- Abrir phpMyAdmin
- Ejecutar el SQL de `create_database.sql`
- Aplicar migraciones: `python manage.py migrate`
- Cargar datos: `python manage.py loaddata fixtures/datos_iniciales.json`

### 6. **Ejecutar el proyecto:**
```bash
python manage.py runserver
```

## ⚠️ Notas Importantes:
- El archivo `.env` NO se sube a Git (está en .gitignore)
- Cada PC debe tener su propio archivo `.env`
- Nunca compartir credenciales de base de datos
