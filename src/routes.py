from flask import jsonify, request, render_template
from services import (
    start_monitor_mode,
    stop_monitor_mode,
    scan_wifi,
    list_interfaces,
    reset_interface,
    deauth_attack,
    save_scan_results_to_csv,
    save_scan_results_to_json,
    capture_handshake  # Importar la función para capturar handshakes
)
import logging
import re

def is_valid_mac_address(mac):
    """Valida que la dirección MAC tenga el formato correcto."""
    pattern = re.compile(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")
    return bool(pattern.match(mac))

def is_valid_interface(interface, available_interfaces):
    """Valida que la interfaz proporcionada sea válida."""
    return interface in available_interfaces

def register_routes(app):
    @app.route("/", methods=["GET"])
    def index():
        """Ruta para cargar la página principal."""
        logging.info("Ruta raíz / llamada")
        return render_template("index.html")

    @app.route("/audit_panel", methods=["GET"])
    def audit_panel():
        """Ruta para cargar el panel de auditoría."""
        logging.info("Ruta /audit_panel llamada")
        return render_template("audit_panel.html")

    @app.route("/monitor_mode", methods=["GET"])
    def monitor_mode():
        """Ruta para cargar la página de modo monitor."""
        logging.info("Ruta /monitor_mode llamada")
        return render_template("monitor_mode.html")

    @app.route("/list_interfaces", methods=["GET"])
    def interfaces():
        """Ruta para listar las interfaces de red disponibles."""
        logging.info("Ruta /list_interfaces llamada")
        interfaces = list_interfaces()
        if not interfaces:
            logging.warning("No se encontraron interfaces de red.")
            return jsonify({"error": "No se encontraron interfaces de red"}), 404
        return jsonify({"interfaces": interfaces}), 200

    @app.route("/start_monitor_mode", methods=["POST"])
    def start_monitor():
        """Ruta para iniciar el modo monitor en una interfaz."""
        interface = request.form.get("interface")
        if not interface:
            logging.warning("Interfaz no proporcionada en /start_monitor_mode")
            return jsonify({"error": "Interfaz no proporcionada"}), 400
        logging.info(f"Iniciando modo monitor en la interfaz: {interface}")
        return start_monitor_mode(interface)

    @app.route("/stop_monitor_mode", methods=["POST"])
    def stop_monitor():
        """Ruta para detener el modo monitor en una interfaz."""
        interface = request.form.get("interface")
        if not interface:
            logging.warning("Interfaz no proporcionada en /stop_monitor_mode")
            return jsonify({"error": "Interfaz no proporcionada"}), 400
        logging.info(f"Deteniendo modo monitor en la interfaz: {interface}")
        return stop_monitor_mode(interface)

    @app.route("/scan_wifi", methods=["GET"])
    def scan():
        """Ruta para escanear redes Wi-Fi usando una interfaz."""
        interface = request.args.get("interface")
        if not interface:
            logging.warning("Interfaz no proporcionada en /scan_wifi")
            return jsonify({"error": "Interfaz no proporcionada"}), 400
        logging.info(f"Escaneando redes Wi-Fi con la interfaz: {interface}")
        networks, status_code = scan_wifi(interface)
        if status_code != 200:
            return jsonify(networks), status_code

        # Guardar los resultados en CSV y JSON
        save_scan_results_to_csv(networks)
        save_scan_results_to_json(networks)
        logging.info(f"Resultados guardados en scan_results.csv y scan_results.json")
        return jsonify({"networks": networks}), 200

    @app.route("/reset_interface", methods=["POST"])
    def reset():
        """Ruta para reiniciar una interfaz de red."""
        interface = request.form.get("interface")
        if not interface:
            logging.warning("Interfaz no proporcionada en /reset_interface")
            return jsonify({"error": "Interfaz no proporcionada"}), 400
        logging.info(f"Reiniciando la interfaz: {interface}")
        return reset_interface(interface)

    @app.route("/deauth_attack", methods=["POST"])
    def deauth():
        """Ruta para ejecutar un ataque de desautenticación."""
        data = request.get_json()
        if not data:
            logging.error("Solicitud inválida: no se recibió un cuerpo JSON.")
            return jsonify({"error": "Solicitud inválida. Proporcione datos en formato JSON."}), 400

        interface = data.get("interface")
        bssid = data.get("bssid")
        client_mac = data.get("client_mac", None)  # Permitir que client_mac sea opcional

        available_interfaces = list_interfaces()  # Obtener interfaces disponibles

        # Validaciones de los datos proporcionados
        if not interface or not is_valid_interface(interface, available_interfaces):
            logging.error(f"Interfaz inválida o no proporcionada: {interface}")
            return jsonify({"error": "Interfaz inválida o no proporcionada"}), 400
        if not bssid or not is_valid_mac_address(bssid):
            logging.error(f"BSSID inválido o no proporcionado: {bssid}")
            return jsonify({"error": "BSSID inválido o no proporcionado"}), 400
        if client_mac and not is_valid_mac_address(client_mac):
            logging.error(f"Dirección MAC del cliente inválida: {client_mac}")
            return jsonify({"error": "Dirección MAC del cliente inválida"}), 400

        logging.info(f"Solicitud de ataque de desautenticación: Interfaz={interface}, BSSID={bssid}, Cliente={client_mac or 'broadcast'}")
        try:
            deauth_attack(interface, bssid, client_mac)
            return jsonify({"status": "success"}), 200
        except Exception as e:
            logging.error(f"Error en /deauth_attack: {e}")
            return jsonify({"error": "Error al realizar el ataque de desautenticación"}), 500

    @app.route("/capture_handshake", methods=["POST"])
    def capture_handshake_route():
        """Ruta para capturar un handshake."""
        data = request.get_json()
        interface = data.get("interface")
        bssid = data.get("bssid")
        channel = data.get("channel")

        if not interface or not bssid or not channel:
            logging.warning("Datos incompletos en /capture_handshake")
            return jsonify({"error": "Datos incompletos. Se requiere interfaz, BSSID y canal."}), 400

        logging.info(f"Solicitud de captura de handshake: Interfaz={interface}, BSSID={bssid}, Canal={channel}")
        try:
            response, status = capture_handshake(interface, bssid, channel)
            return jsonify(response), status
        except Exception as e:
            logging.error(f"Error en /capture_handshake: {e}")
            return jsonify({"error": "Error al capturar el handshake"}), 500
        
    @app.route("/execute_command", methods=["POST"])
    def execute_command_route():
        """Ejecuta un comando recibido desde el cliente."""
        data = request.get_json()
        command = data.get("command")

        if not command:
            return jsonify({"error": "No se recibió un comando válido."}), 400
        try:
            # Ejecutar el comando utilizando subprocess
            result = subprocess.run(
                command.split(), capture_output=True, text=True, check=True
            )
            return jsonify({"output": result.stdout.strip()}), 200
        except subprocess.CalledProcessError as e:
            return jsonify({"error": e.stderr.strip()}), 500
        
    @app.route("/cli", methods=["GET"])
    def cli():
        """Ruta para la interfaz CLI."""
        return render_template("cli.html")