# 🚀 Subir Cambios a GitHub - AHORA

## 📝 Cambio Realizado

Se actualizó `app/config.py` para agregar configuración SSL requerida por PostgreSQL en Render.

## 💻 Comandos para Ejecutar

### Opción 1: Desde tu Terminal (Recomendado)

Abre tu terminal en la carpeta del proyecto y ejecuta:

```bash
# 1. Ir a la carpeta del proyecto
cd web-RehabSystem

# 2. Ver qué archivos cambiaron
git status

# 3. Agregar el archivo modificado
git add app/config.py

# 4. Hacer commit con mensaje descriptivo
git commit -m "Fix: Agregar configuración SSL para PostgreSQL en Render"

# 5. Subir a GitHub
git push origin main
```

### Opción 2: Si estás en otra carpeta

```bash
# Ajusta la ruta según donde estés
cd ruta/a/tu/proyecto/web-RehabSystem

# Luego ejecuta los comandos de arriba
git status
git add app/config.py
git commit -m "Fix: Agregar configuración SSL para PostgreSQL en Render"
git push origin main
```

## ✅ Verificar que Funcionó

Después de ejecutar `git push`, deberías ver:

```
Enumerating objects: 7, done.
Counting objects: 100% (7/7), done.
Delta compression using up to 8 threads
Compressing objects: 100% (4/4), done.
Writing objects: 100% (4/4), 456 bytes | 456.00 KiB/s, done.
Total 4 (delta 3), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (3/3), completed with 3 local objects.
To https://github.com/tu-usuario/web-RehabSystem.git
   abc1234..def5678  main -> main
```

## 🔄 Qué Pasará Después

1. **GitHub recibe los cambios** (inmediato)
2. **Render detecta el push** (1-2 minutos)
3. **Render inicia redeploy** (5-10 minutos)
4. **Aplicación se reinicia** con la nueva configuración

## 📊 Monitorear en Render

1. Ve a: https://dashboard.render.com
2. Click en tu Web Service (web-rehabsystem-1)
3. Click en **"Logs"**
4. Verás:
   ```
   ==> Detected new commit
   ==> Building...
   ==> Deploying...
   ```

## 🎯 Resultado Esperado

Después del redeploy, el error de SSL desaparecerá y podrás hacer login sin problemas.

## 🚨 Si Git Pide Credenciales

### Si pide usuario y contraseña:

```bash
# Usuario: tu nombre de usuario de GitHub
# Contraseña: tu Personal Access Token (NO tu contraseña de GitHub)
```

### Si no tienes Personal Access Token:

1. Ve a: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Selecciona: `repo` (acceso completo)
4. Click "Generate token"
5. **Copia el token** (solo se muestra una vez)
6. Úsalo como contraseña cuando Git lo pida

### Configurar Git para recordar credenciales:

```bash
git config --global credential.helper store
```

## 🔍 Verificar Estado Actual

Antes de hacer push, verifica:

```bash
# Ver qué archivos cambiaron
git status

# Ver los cambios específicos
git diff app/config.py

# Ver últimos commits
git log --oneline -5
```

## 💡 Comandos Útiles

```bash
# Si necesitas deshacer cambios (antes de commit)
git checkout app/config.py

# Si necesitas deshacer el último commit (después de commit)
git reset --soft HEAD~1

# Ver historial de commits
git log --oneline --graph --all

# Ver ramas
git branch -a
```

## 📞 Resumen de 3 Comandos

Si ya estás en la carpeta correcta:

```bash
git add app/config.py
git commit -m "Fix: SSL config for PostgreSQL"
git push origin main
```

**Eso es todo. Ejecuta estos 3 comandos y espera el redeploy.**

---

**Tiempo total**: 2 minutos para subir + 10 minutos de redeploy = 12 minutos
