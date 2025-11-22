# 🚀 Guía de Despliegue - AWS EC2

## 📋 Información del Servidor

- **IP Pública:** 23.23.159.25
- **URLs:**
  - Admin: http://23.23.159.25/admin/
  - Login: http://23.23.159.25/login/
  - Dashboard: http://23.23.159.25/

## 🔐 Credenciales

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin | admin123 | Administrador |
| vendedor1 | vendedor123 | Vendedor |
| bodeguero1 | bodeguero123 | Bodeguero |

## 🔄 Actualizar Proyecto en el Servidor

### 1. En tu PC local:
```bash
git add .
git commit -m "Descripción de cambios"
git push origin main
```

### 2. En el servidor EC2 (conectar por SSH):
```bash
cd ~/Proyecto_Back_End
#Si dice permision denied ejecutar:
 chmod +x deploy.sh
# luego ejecutar:
./deploy.sh
```

**El script automáticamente:**
- ✅ Descarta cambios locales del servidor (git reset --hard)
- ✅ Descarga los cambios desde GitHub (git pull)
- ✅ Instala dependencias nuevas (pip install)
- ✅ Aplica migraciones de BD (migrate)
- ✅ Recolecta archivos estáticos (collectstatic)
- ✅ Reinicia el servidor (systemctl restart)

**⚠️ Nota:** El script descarta TODOS los cambios locales del servidor. Asegúrate de hacer commit en tu PC antes de ejecutarlo.

## 🛠️ Comandos Útiles del Servidor

```bash
# Ver estado del servicio
sudo systemctl status dulceria

# Reiniciar servidor manualmente
sudo systemctl restart dulceria

# Ver logs en tiempo real
sudo journalctl -u dulceria -f

# Detener servidor
sudo systemctl stop dulceria

# Iniciar servidor
sudo systemctl start dulceria
```

## 📝 Notas Importantes

- El servidor se inicia automáticamente al reiniciar EC2
- DEBUG está en False (producción)
- Nginx sirve archivos estáticos en puerto 80
- Gunicorn corre la aplicación con 3 workers
