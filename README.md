WiFi Audit Tool
Una herramienta para auditar redes Wi-Fi de manera eficiente, diseñada para ser utilizada en entornos controlados y de investigación. Proporciona funcionalidades como la configuración del modo monitor, escaneo de redes, captura de handshakes y ataques de desautenticación. Nota: Esta herramienta debe usarse únicamente en entornos donde tengas permiso explícito.

Requisitos Previos
1. Dependencias
Antes de ejecutar la aplicación, asegúrate de que las siguientes herramientas estén instaladas:

Python 3.10+
airmon-ng (parte de aircrack-ng)
iwlist y iwconfig
Scapy (pip install scapy)
2. Permisos
Ejecuta la aplicación con permisos de superusuario (root), ya que algunas operaciones requieren acceso administrativo.

Instalación:

1. Clona el repositorio:
    ```bash
    git clone https://github.com/Yunmanjecc/wifi_audit.git
    cd wifi_audit
    ```

2. Crea y activa un entorno virtual:
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate


3. Instala las dependencias:
pip install -r requirements.txt

## Uso

1. Ejecuta la aplicación:
sudo python3 app.py

2. Abre tu navegador y ve a `http://127.0.0.1:5000`.


README.md
WiFi Audit Tool
Una herramienta para auditar redes Wi-Fi de manera eficiente, diseñada para ser utilizada en entornos controlados y de investigación. Proporciona funcionalidades como la configuración del modo monitor, escaneo de redes, captura de handshakes y ataques de desautenticación. Nota: Esta herramienta debe usarse únicamente en entornos donde tengas permiso explícito.

Requisitos Previos
1. Dependencias
Antes de ejecutar la aplicación, asegúrate de que las siguientes herramientas estén instaladas:

Python 3.10+
airmon-ng (parte de aircrack-ng)
iwlist y iwconfig
Scapy (pip install scapy)
2. Permisos
Ejecuta la aplicación con permisos de superusuario (root), ya que algunas operaciones requieren acceso administrativo.

Instalación
Clona este repositorio:

bash
Copiar código
git clone <URL del repositorio>
cd wifi_audit
Crea y activa un entorno virtual:

bash
Copiar código
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
Instala las dependencias:

bash
Copiar código
pip install -r requirements.txt
Verifica las dependencias del sistema:

bash
Copiar código
python app.py --check
Uso
1. Iniciar la Aplicación
Ejecuta el servidor Flask:

bash
Copiar código
sudo python app.py
El servidor estará disponible en http://127.0.0.1:5000.

2. Funcionalidades Principales
Modo Monitor

Dirígete a la página de Modo Monitor (/monitor_mode).
Selecciona una interfaz de red inalámbrica de la lista.

Usa los botones para:
    Iniciar Modo Monitor: Configura la interfaz en modo monitor utilizando airmon-ng.
    
    Detener Modo Monitor: Restaura la interfaz al modo gestionado.
    
    Restaurar Interfaz: Reinicia la configuración de la interfaz.

Escaneo de Redes
En el panel principal o en el Audit Panel:
    Selecciona una interfaz configurada en modo monitor.
    Haz clic en "Escanear Redes WiFi".
Se mostrará una lista de redes disponibles (SSID, BSSID, Canal, Calidad y Encriptación).

Captura de Handshake
En el Audit Panel:
    Proporciona el BSSID y el canal de la red objetivo.
    Haz clic en "Capturar Handshake".
    Los archivos capturados se guardarán en /tmp/handshake*.
Ataque de Desautenticación
    En el Audit Panel o página principal:
    Selecciona la interfaz en modo monitor.
    Proporciona el BSSID del AP y, opcionalmente, la dirección MAC del cliente.
    Haz clic en "Ataque de Desautenticación".
    Se enviarán paquetes de desautenticación al AP o al cliente específico.

## Estructura del Código
wifi_audit/
├── app.py              # Inicializa el servidor Flask
├── routes.py           # Define las rutas del servidor
├── services.py         # Funciones principales para interactuar con el sistema
├── static/             # Archivos estáticos (CSS, JS)
│   ├── css/
│   └── js/
├── templates/          # Plantillas HTML (interfaz)
└── requirements.txt    # Dependencias de Python

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que te gustaría hacer.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.
