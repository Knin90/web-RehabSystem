# 🧪 Guía de Pruebas - Módulo de Cámara

## ✅ Checklist de Pruebas

### Pruebas Básicas

- [ ] **Acceso a la página**
  - Iniciar sesión como terapeuta
  - Navegar a "Sesión Activa"
  - Verificar que la página carga correctamente

- [ ] **Iniciar cámara**
  - Hacer clic en "Iniciar Cámara"
  - Verificar que aparece el diálogo de permisos
  - Aceptar permisos
  - Verificar que el video se muestra

- [ ] **Estado visual**
  - Badge cambia a "Conectado" (verde)
  - Placeholder desaparece
  - Botón cambia a "Detener Cámara" (rojo)
  - Botón "Capturar Foto" se habilita

- [ ] **Capturar foto**
  - Hacer clic en "Capturar Foto"
  - Verificar notificación de éxito
  - Revisar consola (F12) para ver el dataURL

- [ ] **Pantalla completa**
  - Hacer clic en "Pantalla Completa"
  - Verificar que el video se expande
  - Presionar ESC para salir

- [ ] **Detener cámara**
  - Hacer clic en "Detener Cámara"
  - Verificar que el video se detiene
  - Badge cambia a "Desconectado"
  - Placeholder reaparece

### Pruebas de Métricas

- [ ] **Tiempo de sesión**
  - Verificar que el contador inicia en 00:00
  - Verificar que incrementa cada segundo
  - Formato correcto MM:SS

- [ ] **Contador de repeticiones**
  - Verificar que inicia en 0
  - Verificar que incrementa aleatoriamente

- [ ] **Calidad de movimiento**
  - Verificar que muestra porcentaje
  - Verificar que cambia dinámicamente

### Pruebas de Notas

- [ ] **Escribir nota**
  - Escribir texto en el área de notas
  - Hacer clic en "Guardar nota"
  - Verificar notificación de éxito

- [ ] **Nota vacía**
  - Intentar guardar sin escribir
  - Verificar que muestra alerta

### Pruebas de Errores

- [ ] **Permisos denegados**
  - Denegar permisos de cámara
  - Verificar mensaje de error apropiado

- [ ] **Sin cámara**
  - Desconectar cámara física
  - Intentar iniciar
  - Verificar mensaje de error

- [ ] **Cámara en uso**
  - Abrir otra app que use la cámara
  - Intentar iniciar en RehabSystem
  - Verificar mensaje de error

### Pruebas de Navegadores

- [ ] **Chrome**
  - Versión: _______
  - Estado: ✅ / ❌

- [ ] **Firefox**
  - Versión: _______
  - Estado: ✅ / ❌

- [ ] **Edge**
  - Versión: _______
  - Estado: ✅ / ❌

- [ ] **Safari** (macOS/iOS)
  - Versión: _______
  - Estado: ✅ / ❌

### Pruebas Responsive

- [ ] **Desktop (1920x1080)**
  - Layout correcto
  - Controles visibles
  - Video proporcional

- [ ] **Tablet (768x1024)**
  - Layout adaptado
  - Controles accesibles
  - Video responsive

- [ ] **Móvil (375x667)**
  - Layout vertical
  - Controles apilados
  - Video ajustado

### Pruebas de Rendimiento

- [ ] **Uso de CPU**
  - Abrir Task Manager
  - Verificar uso < 50%

- [ ] **Uso de RAM**
  - Verificar uso < 500 MB

- [ ] **Fluidez de video**
  - Verificar 30 FPS mínimo
  - Sin lag o congelamiento

---

## 🐛 Reporte de Bugs

### Formato de Reporte

```
**Título:** [Descripción breve del bug]

**Descripción:**
[Descripción detallada del problema]

**Pasos para reproducir:**
1. [Paso 1]
2. [Paso 2]
3. [Paso 3]

**Resultado esperado:**
[Qué debería pasar]

**Resultado actual:**
[Qué está pasando]

**Navegador:**
[Chrome 120 / Firefox 121 / etc.]

**Sistema Operativo:**
[Windows 11 / macOS 14 / etc.]

**Capturas:**
[Adjuntar si es posible]
```

---

## 📊 Resultados de Pruebas

### Fecha: __________
### Probador: __________

| Categoría | Pruebas | Pasadas | Fallidas | % |
|-----------|---------|---------|----------|---|
| Básicas | 6 | | | |
| Métricas | 3 | | | |
| Notas | 2 | | | |
| Errores | 3 | | | |
| Navegadores | 4 | | | |
| Responsive | 3 | | | |
| Rendimiento | 3 | | | |
| **TOTAL** | **24** | | | |

---

## 🎯 Criterios de Aceptación

Para considerar el módulo como "Aprobado":

✅ Mínimo 90% de pruebas pasadas  
✅ Funciona en Chrome, Firefox y Edge  
✅ Responsive en móvil y tablet  
✅ Sin bugs críticos  
✅ Rendimiento aceptable (< 50% CPU)  

---

## 📝 Notas Adicionales

[Espacio para notas del probador]

---

**Última actualización:** Diciembre 2, 2024
