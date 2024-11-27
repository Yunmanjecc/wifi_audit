# WiFi Audit Tool

Esta es una herramienta de auditoría WiFi basada en Flask que interactúa con herramientas como `aircrack-ng` para realizar auditorías de redes WiFi.

## Estructura del Proyecto
wifi_audit/
│
├── src/
│   ├── app.py
│   ├── routes.py
│   ├── services.py
│   ├── utils.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── audit_panel.html
│   │   └── monitor_mode.html
│   ├── static/
│   │   ├── js/
│   │   │   └── scripts.js
│   │   ├── css/
│   │   │   └── styles.css
│   │   └── images/
│   │       └── logo.png
│   └── logs/
│       └── audit_logs.log
├── README.md
├── requirements.txt
├── .gitignore
└── venv/  # Entorno virtual (si necesario, fuera de src)


## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/tu_usuario/wifi_audit.git
    cd wifi_audit
    ```

2. Crea y activa un entorno virtual:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

1. Ejecuta la aplicación:
    ```bash
    flask run
    ```

2. Abre tu navegador y ve a `http://127.0.0.1:5000`.

## Estructura del Código

- `app.py`: Archivo principal para inicializar Flask.
- `routes.py`: Registro y gestión de rutas Flask.
- `services.py`: Funciones y lógica del backend.
- `utils.py`: Funciones reutilizables y utilidades.
- `templates/`: Carpeta para las plantillas HTML.
- `static/`: Carpeta para archivos estáticos.
- `logs/`: Carpeta para los logs.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que te gustaría hacer.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.
