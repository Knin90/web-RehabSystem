# Estructura del Proyecto: Rehab System

A continuación se detalla la estructura de archivos y directorios del proyecto, junto con una breve descripción del propósito de cada componente.

```
rehab-system/
│
├── app/                  # Paquete principal de la aplicación Flask (Patrón de Fábrica de Aplicaciones)
│   ├── __init__.py       # Inicializa la aplicación Flask y sus extensiones (fábrica de la aplicación).
│   ├── config.py         # Clases de configuración para diferentes entornos (desarrollo, producción, testing).
│   ├── forms.py          # Clases de formularios (ej. WTForms) para la entrada de datos del usuario.
│   ├── models.py         # Modelos de la base de datos (ej. SQLAlchemy) que definen la estructura de los datos.
│   └── routes.py         # Define las rutas (endpoints) de la aplicación y la lógica de las vistas.
│
├── rehab-system/         # Directorio legado o posible módulo con una app simple.
│   ├── app.py            # Una aplicación Flask simple y autocontenida (posiblemente versión inicial).
│   ├── static/           # Contiene archivos estáticos que se sirven directamente al cliente.
│   │   ├── css/          # Hojas de estilo CSS.
│   │   │   └── landing.css
│   │   ├── images/       # Imágenes del proyecto.
│   │   │   └── banner-principal.png
│   │   └── js/           # Archivos de JavaScript.
│   │       └── landing.js
│   └── templates/        # Plantillas HTML (usadas por Flask para renderizar las vistas).
│       ├── dashboard_admin.html
│       ├── dashboard_paciente.html
│       ├── dashboard_terapeuta.html
│       ├── index.html
│       ├── login.html
│       └── seleccionar_modulo.html
│
├── venv/                 # Directorio del entorno virtual de Python (ignorado).
│
├── .env                  # Archivo para variables de entorno (no versionado).
├── .env.testing          # Variables de entorno específicas para el entorno de testing.
├── .gitignore            # Especifica los archivos y directorios a ignorar por Git.
├── requirements.txt      # Lista de dependencias de Python para el proyecto.
├── run.py                # Script para ejecutar la aplicación Flask (usando la fábrica de 'app').
├── seed_data.py          # Script para poblar la base de datos con datos iniciales o de prueba.
└── test_env.py           # Script para verificar o cargar variables de entorno de prueba.
```

## Resumen de Componentes

### `app/`
Este directorio sigue el patrón de "Application Factory" de Flask. Es la forma recomendada para estructurar aplicaciones escalables. Contiene la lógica principal de la aplicación, separada en módulos:
- **`__init__.py`**: Crea y configura la instancia de la aplicación Flask.
- **`config.py`**: Gestiona las diferentes configuraciones (desarrollo, producción).
- **`models.py`**: Define las tablas y la estructura de la base de datos.
- **`routes.py`**: Maneja las peticiones web y la lógica de negocio.
- **`forms.py`**: Define los formularios para interactuar con el usuario.

### `rehab-system/`
Este directorio parece contener una versión más antigua o simplificada de la aplicación (`app.py`). Los directorios `static` y `templates` están asociados a esta estructura, aunque la nueva aplicación en `app/` ha sido configurada para usarlos también.

### Archivos Raíz
- **`run.py`**: Es el punto de entrada para iniciar el servidor de desarrollo. Importa la fábrica `create_app` desde el paquete `app`.
- **`requirements.txt`**: Fundamental para la reproducibilidad del entorno, lista todas las librerías de Python necesarias.
- **`.env`**: Almacena configuraciones sensibles o específicas del entorno, como claves de API o credenciales de base de datos.
- **`seed_data.py`**: Utilidad para crear datos de ejemplo, muy útil para el desarrollo y las pruebas.
