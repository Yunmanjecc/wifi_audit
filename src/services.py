import subprocess
import json
import logging
import os
from scapy.all import sendp, Dot11, RadioTap, Dot11Deauth
import csv

def check_dependencies():
    """Verifica que todas las dependencias necesarias estén instaladas."""
    dependencies = ['airmon-ng', 'iwlist', 'iwconfig']
    missing = []

    for tool in dependencies:
        result = subprocess.run(['which', tool], capture_output=True, text=True)
        if result.returncode != 0:
            missing.append(tool)

    if os.geteuid() != 0:
        missing.append("Permisos de root (necesarios para ejecutar la aplicación)")

    if missing:
        return False, missing
    return True, []

def execute_command(command):
    """Ejecuta un comando en la terminal y maneja errores."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al ejecutar comando: {' '.join(command)}\n{e.stderr}")
        raise Exception(f"Fallo al ejecutar {' '.join(command)}: {e.stderr}")

def list_interfaces():
    """Lista todas las interfaces de red disponibles."""
    try:
        result = execute_command(["ip", "link", "show"])
        interfaces = [
            line.split(": ")[1].split(":")[0]
            for line in result.split('\n')
            if ": " in line and "lo" not in line
        ]
        logging.info(f"Interfaces disponibles: {interfaces}")
        return interfaces
    except Exception as e:
        logging.error(f"Error al listar interfaces: {e}")
        return []

def start_monitor_mode(interface):
    """Cambia la interfaz al modo monitor."""
    try:
        logging.info(f"Configurando la interfaz {interface} en modo monitor...")
        execute_command(["sudo", "airmon-ng", "check", "kill"])
        execute_command(["sudo", "ip", "link", "set", interface, "down"])
        execute_command(["sudo", "iwconfig", interface, "mode", "monitor"])
        execute_command(["sudo", "ip", "link", "set", interface, "up"])
        return {"message": f"Interfaz {interface} configurada en modo monitor"}, 200
    except Exception as e:
        logging.error(f"Error al iniciar modo monitor en {interface}: {e}")
        return {"error": str(e)}, 500

def stop_monitor_mode(interface):
    """Cambia la interfaz al modo gestionado."""
    try:
        logging.info(f"Restaurando la interfaz {interface} a modo gestionado...")
        execute_command(["sudo", "ip", "link", "set", interface, "down"])
        execute_command(["sudo", "iwconfig", interface, "mode", "managed"])
        execute_command(["sudo", "ip", "link", "set", interface, "up"])
        return {"message": f"Interfaz {interface} configurada en modo gestionado"}, 200
    except Exception as e:
        logging.error(f"Error al detener modo monitor en {interface}: {e}")
        return {"error": str(e)}, 500

def reset_interface(interface):
    """Reinicia la interfaz de red."""
    try:
        logging.info(f"Reiniciando la interfaz {interface}...")
        execute_command(["sudo", "ip", "link", "set", interface, "down"])
        execute_command(["sudo", "ip", "link", "set", interface, "up"])
        return {"message": f"Interfaz {interface} reiniciada"}, 200
    except Exception as e:
        logging.error(f"Error al reiniciar la interfaz: {e}")
        return {"error": str(e)}, 500

def scan_wifi(interface):
    """Escanea las redes Wi-Fi disponibles."""
    logging.info(f"Escaneando redes con la interfaz {interface}...")

    try:
        execute_command(["sudo", "ip", "link", "set", interface, "down"])
        execute_command(["sudo", "iwconfig", interface, "mode", "managed"])
        execute_command(["sudo", "ip", "link", "set", interface, "up"])

        result = execute_command(["sudo", "iwlist", interface, "scan"])
        networks = parse_iwlist_output(result)

        execute_command(["sudo", "ip", "link", "set", interface, "down"])
        execute_command(["sudo", "iwconfig", interface, "mode", "monitor"])
        execute_command(["sudo", "ip", "link", "set", interface, "up"])

        logging.info(f"Redes encontradas: {len(networks)}")
        return networks, 200
    except Exception as e:
        logging.error(f"Error al escanear redes: {e}")
        return {"error": str(e)}, 500

def parse_iwlist_output(output):
    """Parsea la salida del comando iwlist para extraer información de redes."""
    networks = []
    network = {}
    for line in output.split('\n'):
        if "Cell" in line:
            if network:
                networks.append(network)
            network = {}
            parts = line.split()
            network["BSSID"] = parts[4]
        elif "ESSID" in line:
            network["SSID"] = line.split(":")[1].strip('"')
        elif "Channel" in line:
            network["Channel"] = line.split(":")[1]
        elif "Quality" in line:
            network["Quality"] = line.split("=")[1].split()[0]
        elif "Encryption key" in line:
            network["Encryption"] = "on" if "on" in line else "off"
    if network:
        networks.append(network)
    return networks

def capture_handshake(interface, bssid, channel):
    """Captura un handshake en una red WiFi específica."""
    logging.info(f"Iniciando captura de handshake en BSSID: {bssid}, Canal: {channel} usando {interface}...")
    try:
        execute_command(["sudo", "iwconfig", interface, "channel", channel])
        airodump_command = [
            "sudo", "airodump-ng",
            "--bssid", bssid,
            "--channel", channel,
            "--write", "/tmp/handshake",
            interface
        ]
        logging.info(f"Ejecutando: {' '.join(airodump_command)}")
        subprocess.Popen(airodump_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return {"message": "Captura de handshake iniciada. Revisa los archivos en /tmp/handshake*"}, 200
    except Exception as e:
        logging.error(f"Error al capturar handshake: {e}")
        return {"error": str(e)}, 500