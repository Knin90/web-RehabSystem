# 📊 DIAGRAMA DE CASOS DE USO - Sistema de Rehabilitación

## 🎯 Actores del Sistema

### 1. **Administrador**
- Gestiona usuarios, terapeutas y pacientes
- Configura el sistema
- Exporta datos y reportes

### 2. **Terapeuta**
- Gestiona pacientes asignados
- Crea y asigna rutinas de ejercicios
- Realiza sesiones de terapia con captura de video/foto
- Comparte videos con pacientes
- Visualiza progreso de pacientes

### 3. **Paciente**
- Visualiza rutinas asignadas
- Realiza ejercicios de terapia
- Captura videos/fotos de sus sesiones
- Comparte videos con terapeuta
- Consulta su progreso

---

## 📋 CASOS DE USO POR ACTOR

### 🔐 **CASOS DE USO COMUNES (Todos los actores)**

```
┌─────────────────────────────────────────┐
│  CU-001: Iniciar Sesión                 │
│  Actor: Administrador, Terapeuta,       │
│         Paciente                         │
│  Descripción: Autenticación en sistema  │
│  Precondición: Usuario registrado       │
│  Postcondición: Acceso al dashboard     │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-002: Cerrar Sesión                  │
│  Actor: Administrador, Terapeuta,       │
│         Paciente                         │
│  Descripción: Salir del sistema         │
│  Precondición: Sesión activa            │
│  Postcondición: Sesión terminada        │
└─────────────────────────────────────────┘
```

---

### 👨‍💼 **CASOS DE USO DEL ADMINISTRADOR**

```
┌─────────────────────────────────────────┐
│  CU-ADM-001: Gestionar Usuarios         │
│  Actor: Administrador                    │
│  Descripción: CRUD de usuarios          │
│  Incluye:                                │
│    - Crear usuario                       │
│    - Editar usuario                      │
│    - Activar/Desactivar usuario         │
│    - Eliminar usuario                    │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-ADM-002: Gestionar Terapeutas       │
│  Actor: Administrador                    │
│  Descripción: Administrar terapeutas    │
│  Incluye:                                │
│    - Agregar terapeuta                   │
│    - Asignar especialidad                │
│    - Ver lista de terapeutas             │
│    - Ver pacientes por terapeuta         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-ADM-003: Gestionar Pacientes        │
│  Actor: Administrador                    │
│  Descripción: Administrar pacientes     │
│  Incluye:                                │
│    - Agregar paciente                    │
│    - Asignar diagnóstico                 │
│    - Configurar sesiones totales         │
│    - Ver progreso de pacientes           │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-ADM-004: Configurar Sistema         │
│  Actor: Administrador                    │
│  Descripción: Ajustar configuraciones   │
│  Incluye:                                │
│    - Duración de sesiones                │
│    - Notificaciones                      │
│    - Respaldos automáticos               │
│    - Seguridad (timeout, 2FA)            │
│    - Visión artificial (IA)              │
│    - Apariencia (tema, idioma)           │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-ADM-005: Exportar Datos             │
│  Actor: Administrador                    │
│  Descripción: Generar reportes CSV      │
│  Incluye:                                │
│    - Exportar usuarios                   │
│    - Exportar pacientes                  │
│    - Exportar terapeutas                 │
│    - Exportar ejercicios                 │
│    - Exportar todo (completo)            │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-ADM-006: Ver Dashboard Admin        │
│  Actor: Administrador                    │
│  Descripción: Visualizar estadísticas   │
│  Incluye:                                │
│    - Total usuarios                      │
│    - Total pacientes activos             │
│    - Total terapeutas                    │
│    - Estadísticas generales              │
└─────────────────────────────────────────┘
```

---

### 🧑‍⚕️ **CASOS DE USO DEL TERAPEUTA**

```
┌─────────────────────────────────────────┐
│  CU-TER-001: Ver Dashboard Terapeuta    │
│  Actor: Terapeuta                        │
│  Descripción: Visualizar resumen        │
│  Incluye:                                │
│    - Pacientes asignados                 │
│    - Sesiones programadas                │
│    - Estadísticas de progreso            │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-TER-002: Gestionar Pacientes        │
│  Actor: Terapeuta                        │
│  Descripción: Ver y gestionar pacientes │
│  Incluye:                                │
│    - Ver lista de pacientes              │
│    - Ver detalles de paciente            │
│    - Ver progreso de paciente            │
│    - Ver historial de sesiones           │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-TER-003: Crear Rutina de Ejercicios │
│  Actor: Terapeuta                        │
│  Descripción: Diseñar rutina            │
│  Incluye:                                │
│    - Seleccionar ejercicios              │
│    - Configurar series/repeticiones      │
│    - Establecer tiempo de descanso       │
│    - Definir dificultad                  │
│    - Agregar notas                       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-TER-004: Asignar Rutina a Paciente  │
│  Actor: Terapeuta                        │
│  Descripción: Asignar rutina creada     │
│  Precondición: Rutina creada             │
│  Incluye:                                │
│    - Seleccionar paciente                │
│    - Seleccionar rutina                  │
│    - Confirmar asignación                │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-TER-005: Iniciar Sesión de Terapia  │
│  Actor: Terapeuta                        │
│  Descripción: Realizar sesión con       │
│               captura multimedia         │
│  Incluye:                                │
│    - Seleccionar paciente                │
│    - Capturar fotos                      │
│    - Grabar videos (con/sin audio)       │
│    - Agregar notas                       │
│    - Guardar sesión                      │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-TER-006: Capturar Foto de Sesión    │
│  Actor: Terapeuta                        │
│  Descripción: Tomar foto durante sesión │
│  Precondición: Sesión iniciada           │
│  Incluye:                                │
│    - Acceder a cámara                    │
│    - Capturar imagen                     │
│    - Guardar en base de datos            │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-TER-007: Grabar Video de Sesión     │
│  Actor: Terapeuta                        │
│  Descripción: Grabar video con audio    │
│  Precondición: Sesión iniciada           │
│  Incluye:                                │
│    - Iniciar grabación                   │
│    - Detener grabación                   │
│    - Guardar video permanente            │
│    - Agregar notas                       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-TER-008: Ver Galería de Videos      │
│  Actor: Terapeuta                        │
│  Descripción: Visualizar capturas       │
│  Incluye:                                │
│    - Ver fotos guardadas                 │
│    - Ver videos guardados                │
│    - Filtrar por paciente                │
│    - Reproducir videos                   │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-TER-009: Compartir Video con        │
│              Paciente                    │
│  Actor: Terapeuta                        │
│  Descripción: Enviar video a paciente   │
│  Precondición: Video guardado            │
│  Incluye:                                │
│    - Seleccionar video                   │
│    - Seleccionar paciente                │
│    - Agregar mensaje                     │
│    - Confirmar envío                     │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-TER-010: Ver Videos Compartidos     │
│              por Pacientes               │
│  Actor: Terapeuta                        │
│  Descripción: Recibir videos de         │
│               pacientes                  │
│  Incluye:                                │
│    - Ver lista de videos recibidos       │
│    - Reproducir videos                   │
│    - Marcar como leído                   │
│    - Ver mensaje del paciente            │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-TER-011: Gestionar Citas            │
│  Actor: Terapeuta                        │
│  Descripción: Administrar citas         │
│  Incluye:                                │
│    - Ver calendario                      │
│    - Programar cita                      │
│    - Modificar cita                      │
│    - Cancelar cita                       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-TER-012: Ver Rutinas Creadas        │
│  Actor: Terapeuta                        │
│  Descripción: Gestionar rutinas         │
│  Incluye:                                │
│    - Ver lista de rutinas                │
│    - Editar rutina                       │
│    - Eliminar rutina                     │
│    - Duplicar rutina                     │
└─────────────────────────────────────────┘
```

---

### 🤕 **CASOS DE USO DEL PACIENTE**

```
┌─────────────────────────────────────────┐
│  CU-PAC-001: Ver Dashboard Paciente     │
│  Actor: Paciente                         │
│  Descripción: Visualizar resumen        │
│  Incluye:                                │
│    - Progreso general                    │
│    - Sesiones completadas/totales        │
│    - Diagnóstico                         │
│    - Próximas sesiones                   │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-PAC-002: Ver Rutinas Asignadas      │
│  Actor: Paciente                         │
│  Descripción: Consultar rutinas         │
│  Incluye:                                │
│    - Ver lista de rutinas                │
│    - Ver detalles de rutina              │
│    - Ver ejercicios de rutina            │
│    - Ver series/repeticiones             │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-PAC-003: Iniciar Terapia            │
│  Actor: Paciente                         │
│  Descripción: Realizar ejercicios       │
│  Incluye:                                │
│    - Seleccionar rutina                  │
│    - Seguir instrucciones                │
│    - Capturar progreso                   │
│    - Completar sesión                    │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-PAC-004: Capturar Foto de Ejercicio │
│  Actor: Paciente                         │
│  Descripción: Tomar foto durante        │
│               ejercicio                  │
│  Incluye:                                │
│    - Acceder a cámara                    │
│    - Capturar imagen                     │
│    - Agregar notas                       │
│    - Guardar foto                        │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-PAC-005: Grabar Video de Ejercicio  │
│  Actor: Paciente                         │
│  Descripción: Grabar video con audio    │
│  Incluye:                                │
│    - Iniciar grabación                   │
│    - Detener grabación                   │
│    - Agregar notas                       │
│    - Guardar video permanente            │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-PAC-006: Ver Galería de Videos      │
│  Actor: Paciente                         │
│  Descripción: Visualizar capturas       │
│               propias                    │
│  Incluye:                                │
│    - Ver fotos guardadas                 │
│    - Ver videos guardados                │
│    - Reproducir videos                   │
│    - Ver videos del terapeuta            │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-PAC-007: Compartir Video con        │
│              Terapeuta                   │
│  Actor: Paciente                         │
│  Descripción: Enviar video a terapeuta  │
│  Precondición: Video guardado            │
│  Incluye:                                │
│    - Seleccionar video                   │
│    - Seleccionar terapeuta               │
│    - Agregar mensaje                     │
│    - Confirmar envío                     │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-PAC-008: Ver Videos Compartidos     │
│              por Terapeuta               │
│  Actor: Paciente                         │
│  Descripción: Recibir videos de         │
│               terapeuta                  │
│  Incluye:                                │
│    - Ver lista de videos recibidos       │
│    - Reproducir videos                   │
│    - Marcar como leído                   │
│    - Ver mensaje del terapeuta           │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-PAC-009: Ver Historial de Sesiones  │
│  Actor: Paciente                         │
│  Descripción: Consultar historial       │
│  Incluye:                                │
│    - Ver sesiones completadas            │
│    - Ver fechas de sesiones              │
│    - Ver progreso por sesión             │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-PAC-010: Ver Terapeutas Asignados   │
│  Actor: Paciente                         │
│  Descripción: Consultar terapeutas      │
│  Incluye:                                │
│    - Ver lista de terapeutas             │
│    - Ver especialidad                    │
│    - Ver información de contacto         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-PAC-011: Ver Perfil                 │
│  Actor: Paciente                         │
│  Descripción: Consultar información     │
│               personal                   │
│  Incluye:                                │
│    - Ver datos personales                │
│    - Ver diagnóstico                     │
│    - Ver progreso                        │
│    - Editar información                  │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-PAC-012: Configurar Preferencias    │
│  Actor: Paciente                         │
│  Descripción: Ajustar configuración     │
│  Incluye:                                │
│    - Cambiar contraseña                  │
│    - Configurar notificaciones           │
│    - Ajustar privacidad                  │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CU-PAC-013: Enviar Mensajes            │
│  Actor: Paciente                         │
│  Descripción: Comunicarse con terapeuta │
│  Incluye:                                │
│    - Redactar mensaje                    │
│    - Enviar mensaje                      │
│    - Ver mensajes recibidos              │
└─────────────────────────────────────────┘
```

---

## 🔄 DIAGRAMA DE RELACIONES

```
                    ┌──────────────────┐
                    │     SISTEMA      │
                    │  REHABILITACIÓN  │
                    └──────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼────┐        ┌────▼────┐        ┌────▼────┐
   │  ADMIN  │        │TERAPEUTA│        │PACIENTE │
   └────┬────┘        └────┬────┘        └────┬────┘
        │                  │                   │
        │                  │                   │
   ┌────▼─────────────┐   │              ┌────▼──────────┐
   │ Gestionar        │   │              │ Ver Rutinas   │
   │ Usuarios         │   │              │ Asignadas     │
   │ Terapeutas       │   │              └───────────────┘
   │ Pacientes        │   │
   │ Sistema          │   │              ┌───────────────┐
   │ Exportar Datos   │   │              │ Realizar      │
   └──────────────────┘   │              │ Ejercicios    │
                          │              └───────────────┘
                     ┌────▼──────────┐
                     │ Crear Rutinas │   ┌───────────────┐
                     │ Asignar       │   │ Capturar      │
                     │ Rutinas       │   │ Fotos/Videos  │
                     └───────────────┘   └───────────────┘
                                              │
                     ┌────────────────┐       │
                     │ Iniciar Sesión │◄──────┤
                     │ Capturar       │       │
                     │ Multimedia     │       │
                     └────────────────┘       │
                                              │
                     ┌────────────────┐       │
                     │ Compartir      │◄──────┘
                     │ Videos         │
                     └────────────────┘
```

---

## 📊 MATRIZ DE CASOS DE USO

| ID | Caso de Uso | Admin | Terapeuta | Paciente |
|----|-------------|-------|-----------|----------|
| CU-001 | Iniciar Sesión | ✅ | ✅ | ✅ |
| CU-002 | Cerrar Sesión | ✅ | ✅ | ✅ |
| CU-ADM-001 | Gestionar Usuarios | ✅ | ❌ | ❌ |
| CU-ADM-002 | Gestionar Terapeutas | ✅ | ❌ | ❌ |
| CU-ADM-003 | Gestionar Pacientes | ✅ | ❌ | ❌ |
| CU-ADM-004 | Configurar Sistema | ✅ | ❌ | ❌ |
| CU-ADM-005 | Exportar Datos | ✅ | ❌ | ❌ |
| CU-ADM-006 | Ver Dashboard Admin | ✅ | ❌ | ❌ |
| CU-TER-001 | Ver Dashboard Terapeuta | ❌ | ✅ | ❌ |
| CU-TER-002 | Gestionar Pacientes | ❌ | ✅ | ❌ |
| CU-TER-003 | Crear Rutina | ❌ | ✅ | ❌ |
| CU-TER-004 | Asignar Rutina | ❌ | ✅ | ❌ |
| CU-TER-005 | Iniciar Sesión Terapia | ❌ | ✅ | ❌ |
| CU-TER-006 | Capturar Foto Sesión | ❌ | ✅ | ❌ |
| CU-TER-007 | Grabar Video Sesión | ❌ | ✅ | ❌ |
| CU-TER-008 | Ver Galería Videos | ❌ | ✅ | ❌ |
| CU-TER-009 | Compartir Video | ❌ | ✅ | ❌ |
| CU-TER-010 | Ver Videos Recibidos | ❌ | ✅ | ❌ |
| CU-TER-011 | Gestionar Citas | ❌ | ✅ | ❌ |
| CU-TER-012 | Ver Rutinas Creadas | ❌ | ✅ | ❌ |
| CU-PAC-001 | Ver Dashboard Paciente | ❌ | ❌ | ✅ |
| CU-PAC-002 | Ver Rutinas Asignadas | ❌ | ❌ | ✅ |
| CU-PAC-003 | Iniciar Terapia | ❌ | ❌ | ✅ |
| CU-PAC-004 | Capturar Foto Ejercicio | ❌ | ❌ | ✅ |
| CU-PAC-005 | Grabar Video Ejercicio | ❌ | ❌ | ✅ |
| CU-PAC-006 | Ver Galería Videos | ❌ | ❌ | ✅ |
| CU-PAC-007 | Compartir Video | ❌ | ❌ | ✅ |
| CU-PAC-008 | Ver Videos Recibidos | ❌ | ❌ | ✅ |
| CU-PAC-009 | Ver Historial | ❌ | ❌ | ✅ |
| CU-PAC-010 | Ver Terapeutas | ❌ | ❌ | ✅ |
| CU-PAC-011 | Ver Perfil | ❌ | ❌ | ✅ |
| CU-PAC-012 | Configurar Preferencias | ❌ | ❌ | ✅ |
| CU-PAC-013 | Enviar Mensajes | ❌ | ❌ | ✅ |

---

## 📈 ESTADÍSTICAS

- **Total de Casos de Uso:** 33
- **Casos de Uso Comunes:** 2
- **Casos de Uso Administrador:** 6
- **Casos de Uso Terapeuta:** 12
- **Casos de Uso Paciente:** 13

---

**Fecha de Creación:** 2025-12-07  
**Versión:** 1.0  
**Sistema:** RehabSystem - Sistema de Rehabilitación Física
