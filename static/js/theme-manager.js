/**
 * Gestor de Temas y Configuraciones
 */

// Variable para evitar traducciones múltiples
let translationApplied = false;

// Aplicar tema inmediatamente
applyTheme();

// Aplicar el resto al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Theme Manager iniciado');
    
    // Aplicar configuraciones
    applyTheme();
    applyCompactMode();
    
    // Aplicar idioma solo UNA VEZ
    if (!translationApplied) {
        setTimeout(function() {
            applyLanguage();
            translationApplied = true;
        }, 300);
    }
});

/**
 * Aplicar tema desde configuración
 */
function applyTheme() {
    const theme = getSystemSetting('theme', 'light');
    
    if (theme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
    } else if (theme === 'auto') {
        // Detectar preferencia del sistema
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.setAttribute('data-theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
        }
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
    }
}

/**
 * Aplicar modo compacto
 */
function applyCompactMode() {
    const compactMode = getSystemSetting('compact_mode', 'off');
    
    if (compactMode === 'on') {
        document.documentElement.setAttribute('data-compact', 'true');
    } else {
        document.documentElement.setAttribute('data-compact', 'false');
    }
}

/**
 * Aplicar idioma
 */
function applyLanguage() {
    // Evitar aplicar múltiples veces
    if (translationApplied) {
        console.log('⚠️ Traducción ya aplicada, saltando...');
        return;
    }
    
    const language = getSystemSetting('language', 'es');
    document.documentElement.setAttribute('lang', language);
    
    console.log('🌍 Aplicando idioma:', language);
    
    // Aplicar traducciones
    if (language === 'en') {
        console.log('🇺🇸 Traduciendo a inglés...');
        translateToEnglish();
    } else {
        console.log('🇪🇸 Idioma español (por defecto)');
    }
}

/**
 * Obtener configuración del sistema desde el servidor
 */
function getSystemSetting(key, defaultValue) {
    // Intentar obtener desde localStorage primero (caché)
    const cached = localStorage.getItem(`setting_${key}`);
    if (cached) {
        return cached;
    }
    
    // Si no está en caché, usar valor por defecto
    // En una implementación completa, esto haría una petición AJAX
    return defaultValue;
}

/**
 * Guardar configuración en localStorage (caché)
 */
function saveSettingToCache(key, value) {
    localStorage.setItem(`setting_${key}`, value);
}

/**
 * Cambiar tema manualmente
 */
function setTheme(theme) {
    saveSettingToCache('theme', theme);
    applyTheme();
}

/**
 * Cambiar idioma manualmente
 */
function setLanguage(language) {
    saveSettingToCache('language', language);
    applyLanguage();
}

/**
 * Traducciones completas a inglés
 */
function translateToEnglish() {
    const translations = {
        // ===== MENÚ LATERAL =====
        'Administración': 'Administration',
        'Panel General': 'Dashboard',
        'Usuarios': 'Users',
        'Terapeutas': 'Therapists',
        'Pacientes': 'Patients',
        'Configuración': 'Settings',
        'Exportar Datos': 'Export Data',
        'Cerrar sesión': 'Logout',
        
        // ===== TÍTULOS DE PÁGINA =====
        'Panel de Administración': 'Administration Panel',
        'Configuración del Sistema': 'System Settings',
        'Resumen completo del sistema de rehabilitación': 'Complete overview of the rehabilitation system',
        'Ajustes generales del sistema y sus módulos.': 'General system and module settings.',
        'Descarga información del sistema en formato CSV para análisis externo.': 'Download system information in CSV format for external analysis.',
        
        // ===== DASHBOARD =====
        'Sistema de Gestión Integral': 'Comprehensive Management System',
        'Control completo sobre usuarios, perfiles, estadísticas y configuración del sistema de rehabilitación con visión artificial.': 'Complete control over users, profiles, statistics and configuration of the rehabilitation system with artificial vision.',
        'Panel de control': 'Control Panel',
        'Usuarios y Perfiles': 'Users and Profiles',
        'Progreso del sistema': 'System Progress',
        'Estadísticas del centro': 'Center Statistics',
        'Actividad del Sistema': 'System Activity',
        
        // ===== CONFIGURACIÓN - SECCIONES =====
        'Sesiones de Terapia': 'Therapy Sessions',
        'Notificaciones': 'Notifications',
        'Seguridad': 'Security',
        'Respaldos y Mantenimiento': 'Backups and Maintenance',
        'Visión Artificial': 'Artificial Vision',
        'Interfaz y Apariencia': 'Interface and Appearance',
        
        // ===== CONFIGURACIÓN - SESIONES =====
        'Duración predeterminada (minutos)': 'Default duration (minutes)',
        'Tiempo estándar para cada sesión de rehabilitación': 'Standard time for each rehabilitation session',
        'Sesiones por semana (recomendadas)': 'Sessions per week (recommended)',
        'Tiempo de descanso entre ejercicios (seg)': 'Rest time between exercises (sec)',
        
        // ===== CONFIGURACIÓN - NOTIFICACIONES =====
        'Notificaciones por email': 'Email notifications',
        'Recordatorios de citas (24h antes)': 'Appointment reminders (24h before)',
        'Reportes de progreso semanales': 'Weekly progress reports',
        'Alertas de pacientes inactivos (7 días)': 'Inactive patient alerts (7 days)',
        
        // ===== CONFIGURACIÓN - SEGURIDAD =====
        'Tiempo de sesión (minutos)': 'Session timeout (minutes)',
        'Tiempo antes de cerrar sesión automáticamente': 'Time before automatic logout',
        'Autenticación de dos factores': 'Two-factor authentication',
        'Expiración de contraseñas (90 días)': 'Password expiration (90 days)',
        'Intentos de login permitidos': 'Allowed login attempts',
        
        // ===== CONFIGURACIÓN - RESPALDOS =====
        'Respaldo automático diario': 'Daily automatic backup',
        'Hora de respaldo': 'Backup time',
        'Retención de respaldos (días)': 'Backup retention (days)',
        'Limpieza automática de logs antiguos': 'Automatic cleanup of old logs',
        
        // ===== CONFIGURACIÓN - VISIÓN ARTIFICIAL =====
        'Precisión de detección (%)': 'Detection accuracy (%)',
        'Valor actual': 'Current value',
        'Análisis en tiempo real': 'Real-time analysis',
        'Corrección de postura automática': 'Automatic posture correction',
        'FPS de captura': 'Capture FPS',
        '15 FPS (Bajo)': '15 FPS (Low)',
        '30 FPS (Medio)': '30 FPS (Medium)',
        '60 FPS (Alto)': '60 FPS (High)',
        
        // ===== CONFIGURACIÓN - APARIENCIA =====
        'Tema del sistema': 'System theme',
        'Idioma': 'Language',
        'Modo compacto': 'Compact mode',
        'Claro': 'Light',
        'Oscuro': 'Dark',
        'Automático': 'Automatic',
        'Español': 'Spanish',
        'English': 'English',
        
        // ===== EXPORTAR DATOS =====
        'Exportación Rápida': 'Quick Export',
        'Exportar todos los usuarios del sistema': 'Export all system users',
        'Datos de pacientes y progreso': 'Patient data and progress',
        'Información de terapeutas': 'Therapist information',
        'Catálogo de ejercicios': 'Exercise catalog',
        'Exportación Completa': 'Complete Export',
        'Exportar Todo el Sistema': 'Export Entire System',
        'Descarga un archivo CSV con toda la información del sistema:': 'Download a CSV file with all system information:',
        'usuarios, pacientes, terapeutas y ejercicios.': 'users, patients, therapists and exercises.',
        'Descargar Exportación Completa': 'Download Complete Export',
        'Resumen de Datos': 'Data Summary',
        'Total de Usuarios': 'Total Users',
        'Total de Pacientes': 'Total Patients',
        'Total de Terapeutas': 'Total Therapists',
        'Total de Ejercicios': 'Total Exercises',
        'Información sobre Exportaciones': 'Export Information',
        'Formato CSV': 'CSV Format',
        'Los archivos se exportan en formato CSV (valores separados por comas) con codificación UTF-8.': 'Files are exported in CSV format (comma-separated values) with UTF-8 encoding.',
        'Las contraseñas están encriptadas y no se incluyen en las exportaciones por seguridad.': 'Passwords are encrypted and not included in exports for security.',
        'Actualización': 'Update',
        'Los datos exportados reflejan el estado actual del sistema al momento de la descarga.': 'Exported data reflects the current state of the system at the time of download.',
        
        // ===== BOTONES Y ACCIONES =====
        'Guardar Cambios': 'Save Changes',
        'Gestionar': 'Manage',
        'Editar': 'Edit',
        'Descargar': 'Download',
        'Exportar': 'Export',
        
        // ===== ESTADÍSTICAS =====
        'Usuarios Totales': 'Total Users',
        'Progreso Promedio': 'Average Progress',
        'Completado': 'Completed',
        'Activos': 'Active',
        'Registrados': 'Registered',
        'Sesiones Totales': 'Total Sessions',
        'Citas Hoy': 'Appointments Today',
        'Satisfacción': 'Satisfaction',
        'Usuarios sin completar': 'Incomplete Users',
        'Pendientes': 'Pending',
        'Sesiones Activas': 'Active Sessions',
        
        // ===== PÁGINAS ESPECÍFICAS =====
        // Usuarios
        'Gestión de Usuarios': 'User Management',
        'Lista de usuarios': 'User list',
        'Agregar usuario': 'Add user',
        'Buscar usuario': 'Search user',
        'Nombre': 'Name',
        'Email': 'Email',
        'Rol': 'Role',
        'Estado': 'Status',
        'Acciones': 'Actions',
        'Ver': 'View',
        'Eliminar': 'Delete',
        
        // Terapeutas
        'Gestión de Terapeutas': 'Therapist Management',
        'Lista de terapeutas': 'Therapist list',
        'Agregar terapeuta': 'Add therapist',
        'Especialidad': 'Specialty',
        'Pacientes asignados': 'Assigned patients',
        
        // Pacientes
        'Gestión de Pacientes': 'Patient Management',
        'Lista de pacientes': 'Patient list',
        'Agregar paciente': 'Add patient',
        'Diagnóstico': 'Diagnosis',
        'Progreso': 'Progress',
        'Última sesión': 'Last session',
        
        // Comunes
        'Buscar': 'Search',
        'Filtrar': 'Filter',
        'Nuevo': 'New',
        'Cancelar': 'Cancel',
        'Aceptar': 'Accept',
        'Sí': 'Yes',
        'No': 'No',
        'Todos': 'All',
        'Ninguno': 'None',
        'Seleccionar': 'Select',
        'Fecha': 'Date',
        'Hora': 'Time',
        'Descripción': 'Description',
        'Notas': 'Notes',
        'Comentarios': 'Comments',
        'Detalles': 'Details',
        'Información': 'Information',
        'Configurar': 'Configure',
        'Actualizar': 'Update',
        'Refrescar': 'Refresh',
        'Imprimir': 'Print',
        'Compartir': 'Share',
        'Ayuda': 'Help',
        'Más opciones': 'More options',
        'Menos opciones': 'Less options',
        'Mostrar más': 'Show more',
        'Mostrar menos': 'Show less',
        'Cargar más': 'Load more',
        'Sin resultados': 'No results',
        'Cargando...': 'Loading...',
        'Error': 'Error',
        'Éxito': 'Success',
        'Advertencia': 'Warning',
        'Confirmación': 'Confirmation',
        '¿Está seguro?': 'Are you sure?',
        'Esta acción no se puede deshacer': 'This action cannot be undone'
    };
    
    // Traducir todos los elementos de texto
    translateElements(translations);
    console.log('✅ Traducción a inglés completada');
}

// Portugués removido - solo español e inglés disponibles

/**
 * Función auxiliar para aplicar traducciones
 */
function translateElements(translations) {
    let translatedCount = 0;
    const translatedElements = new Set(); // Para evitar traducir el mismo elemento dos veces
    
    // Función para traducir un elemento preservando HTML interno
    function translateElement(element) {
        // Evitar traducir el mismo elemento múltiples veces
        if (translatedElements.has(element)) {
            return;
        }
        translatedElements.add(element);
        
        // Casos especiales: elementos con íconos (nav-link-custom, btn)
        if (element.classList.contains('nav-link-custom') || 
            element.classList.contains('btn') ||
            element.classList.contains('control-text')) {
            
            // Buscar solo nodos de texto directo (hijos inmediatos)
            for (let i = 0; i < element.childNodes.length; i++) {
                const node = element.childNodes[i];
                if (node.nodeType === Node.TEXT_NODE) {
                    const text = node.textContent.trim();
                    if (text && translations[text]) {
                        // Preservar el espacio inicial si existe
                        const prefix = node.textContent.match(/^\s*/)[0];
                        node.textContent = prefix + translations[text];
                        translatedCount++;
                        break; // Solo traducir el primer nodo de texto
                    }
                }
            }
            return;
        }
        
        // Para otros elementos sin hijos HTML
        if (element.children.length === 0) {
            const text = element.textContent.trim();
            if (text && translations[text]) {
                element.textContent = translations[text];
                translatedCount++;
            }
            return;
        }
        
        // Para elementos con hijos, traducir solo nodos de texto
        for (let i = 0; i < element.childNodes.length; i++) {
            const node = element.childNodes[i];
            if (node.nodeType === Node.TEXT_NODE) {
                const text = node.textContent.trim();
                if (text && translations[text]) {
                    const prefix = node.textContent.match(/^\s*/)[0];
                    const suffix = node.textContent.match(/\s*$/)[0];
                    node.textContent = prefix + translations[text] + suffix;
                    translatedCount++;
                }
            }
        }
    }
    
    // Seleccionar todos los elementos que pueden contener texto
    const selectors = [
        '.nav-link-custom',
        '.control-text',
        '.page-title',
        '.page-description',
        '.card-title',
        '.card-header-custom',
        '.nav-title',
        '.hero-title-admin',
        '.hero-subtitle-admin',
        '.form-label',
        '.form-check-label',
        '.btn:not(.btn-danger)', // Excluir botón de logout para evitar problemas
        '.progress-label',
        '.progress-subtitle',
        '.stat-label',
        '.text-muted',
        'h2', 'h3', 'h4', 'h5', 'h6',
        'p', 'label', 'option', 'small'
    ];
    
    selectors.forEach(selector => {
        document.querySelectorAll(selector).forEach(translateElement);
    });
    
    console.log(`✅ ${translatedCount} elementos traducidos`);
}

/**
 * Traducciones básicas a portugués
 */
function translateToPortuguese() {
    const translations = {
        'Configuración': 'Configuração',
        'Exportar Datos': 'Exportar Dados',
        'Usuarios': 'Usuários',
        'Terapeutas': 'Terapeutas',
        'Pacientes': 'Pacientes',
        'Panel General': 'Painel Geral',
        'Cerrar sesión': 'Sair'
    };
    
    document.querySelectorAll('.nav-link-custom, .control-text').forEach(el => {
        const text = el.textContent.trim();
        if (translations[text]) {
            el.textContent = translations[text];
        }
    });
}

// Escuchar cambios en preferencia de tema del sistema (para modo auto)
if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        const theme = getSystemSetting('theme', 'light');
        if (theme === 'auto') {
            applyTheme();
        }
    });
}
