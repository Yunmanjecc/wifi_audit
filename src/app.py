from flask import Flask, request, jsonify
from routes import register_routes
import os
import logging

# Configuración del archivo de logs
log_path = "../logs/audit_logs.log"  # Ubicación de los logs fuera de src
os.makedirs(os.path.dirname(log_path), exist_ok=True)

logging.basicConfig(
    filename=log_path,
    level=logging.DEBUG,  # Cambiar a DEBUG para mayor detalle en el log
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Configuración del logger de consola
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

# Inicialización de la aplicación Flask
app = Flask(
    __name__,
    template_folder=os.path.abspath('templates'),  # Ruta absoluta para evitar conflictos
    static_folder=os.path.abspath('static')        # Ruta absoluta para recursos estáticos
)

# Registro de rutas desde el módulo de rutas
register_routes(app)

@app.errorhandler(404)
def not_found_error(error):
    """Manejo de error 404 - Recurso no encontrado."""
    logging.warning("Ruta no encontrada")
    return jsonify({"error": "Recurso no encontrado"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejo de error 500 - Error interno del servidor."""
    logging.error("Error interno del servidor")
    return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/list_interfaces', methods=['GET'])
def list_interfaces_route():
    """Ruta para listar interfaces de red disponibles."""
    from services import list_interfaces  # Importar dentro de la ruta para evitar referencias cruzadas
    try:
        interfaces = list_interfaces()
        if not interfaces:
            logging.warning("No se encontraron interfaces disponibles")
            return jsonify({"error": "No se encontraron interfaces disponibles"}), 404
        return jsonify({"interfaces": interfaces}), 200
    except Exception as e:
        logging.error(f"Error al listar interfaces: {e}")
        return jsonify({"error": "Error al listar interfaces"}), 500

@app.route('/scan_wifi', methods=['GET'])
def scan_wifi_route():
    """Ruta para escanear redes Wi-Fi."""
    from services import scan_wifi, save_scan_results_to_csv
    interface = request.args.get('interface')
    if not interface:
        logging.warning("Interfaz no proporcionada en /scan_wifi")
        return jsonify({"error": "Interfaz no proporcionada"}), 400

    logging.info(f"Escaneando redes con la interfaz: {interface}")
    try:
        networks, status_code = scan_wifi(interface)
        if status_code != 200:
            return jsonify(networks), status_code

        # Guardar resultados en CSV y JSON
        from services import save_scan_results_to_json
        save_scan_results_to_csv(networks)
        save_scan_results_to_json(networks)

        return jsonify({"networks": networks}), 200
    except Exception as e:
        logging.error(f"Error al escanear redes: {e}")
        return jsonify({"error": "Error al escanear redes"}), 500

@app.route('/deauth_attack', methods=['POST'])
def deauth_attack_route():
    """Ruta para iniciar un ataque de desautenticación."""
    from services import deauth_attack
    data = request.get_json()

    interface = data.get('interface')
    bssid = data.get('bssid')
    client_mac = data.get('client_mac')

    if not interface or not bssid:
        logging.warning("Interfaz o BSSID no proporcionados en /deauth_attack")
        return jsonify({"error": "Interfaz o BSSID no proporcionados"}), 400

    logging.info(f"Iniciando ataque de desautenticación: interfaz={interface}, BSSID={bssid}, cliente={client_mac}")
    try:
        deauth_attack(interface, bssid, client_mac)
        return jsonify({"status": "Ataque ejecutado exitosamente"}), 200
    except Exception as e:
        logging.error(f"Error al ejecutar el ataque de desautenticación: {e}")
        return jsonify({"error": "Error al ejecutar el ataque de desautenticación"}), 500

if __name__ == "__main__":
    print(f"Template folder: {os.path.abspath(app.template_folder)}")
    logging.info("Servidor Flask iniciado")
    app.run(debug=True, host="0.0.0.0", port=5000)
