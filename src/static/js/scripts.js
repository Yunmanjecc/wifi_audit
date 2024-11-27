document.addEventListener("DOMContentLoaded", () => {
    const interfaceSelect = document.getElementById("interface");
    const resultDiv = document.getElementById("result");

    // Función para manejar errores
    function handleError(message) {
        console.error(message);
        resultDiv.innerHTML = `<pre style="color: red;">Error: ${message}</pre>`;
    }

    // Fetch available interfaces
    fetch("/list_interfaces")
        .then(response => response.json())
        .then(data => {
            interfaceSelect.innerHTML = "";
            const wirelessInterfaces = data.interfaces.filter(iface =>
                iface.startsWith("wl")
            ); // Filtrar solo interfaces inalámbricas
            if (wirelessInterfaces.length === 0) {
                handleError("No se encontraron interfaces inalámbricas.");
                return;
            }
            wirelessInterfaces.forEach(iface => {
                const option = document.createElement("option");
                option.value = iface;
                option.textContent = iface;
                interfaceSelect.appendChild(option);
            });
        })
        .catch(err => handleError(`Error al obtener las interfaces: ${err.message}`));

    // Función para enviar solicitudes POST
    async function postRequest(url, data) {
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json", // Cambiado a JSON para mayor consistencia
                },
                body: JSON.stringify(data),
            });
            return await response.json();
        } catch (error) {
            handleError(`Error en la solicitud POST: ${error.message}`);
        }
    }

    // Función para procesar y mostrar los resultados en una tabla
    function displayNetworks(data) {
        resultDiv.innerHTML = ""; // Limpiar contenido previo

        if (data.networks && data.networks.length > 0) {
            const table = document.createElement("table");
            table.innerHTML = `
                <thead>
                    <tr>
                        <th>SSID</th>
                        <th>BSSID</th>
                        <th>Canal</th>
                        <th>Calidad</th>
                        <th>Encriptación</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.networks.map(network => `
                        <tr>
                            <td>${network.SSID || "N/A"}</td>
                            <td>${network.BSSID || "N/A"}</td>
                            <td>${network.Channel || "N/A"}</td>
                            <td>${network.Quality || "N/A"}</td>
                            <td>${network.Encryption || "N/A"}</td>
                        </tr>
                    `).join("")}
                </tbody>
            `;
            resultDiv.appendChild(table);
        } else {
            resultDiv.innerHTML = "<p>No se encontraron redes disponibles.</p>";
        }
    }

    // Función para escanear redes
    async function scanNetworks() {
        const interface = interfaceSelect.value;

        if (interface) {
            resultDiv.innerHTML = "<p style='color: blue;'>Cargando datos...</p>";
            try {
                const response = await fetch(`/scan_wifi?interface=${encodeURIComponent(interface)}`);
                const data = await response.json();

                if (data.networks) {
                    displayNetworks(data);
                } else {
                    handleError(data.error || "No se encontraron redes.");
                }
            } catch (error) {
                handleError(`Error al escanear redes: ${error.message}`);
            }
        } else {
            handleError("Selecciona una interfaz válida");
        }
    }

    // Función para capturar handshake
    async function captureHandshake() {
        const interface = interfaceSelect.value;
        const bssid = document.getElementById("bssid").value;
        const channel = document.getElementById("channel").value;

        if (!interface || !bssid || !channel) {
            handleError("Todos los campos son obligatorios para capturar el handshake.");
            return;
        }

        const data = {
            interface,
            bssid,
            channel,
        };

        const response = await postRequest("/capture_handshake", data);
        if (response) {
            resultDiv.innerHTML = `<pre>${JSON.stringify(response, null, 2)}</pre>`;
        }
    }

    // Manejar el botón para escanear redes
    document.getElementById("scanNetworksButton").addEventListener("click", scanNetworks);

    // Manejar el botón para captura de handshake
    document.getElementById("captureHandshakeButton").addEventListener("click", captureHandshake);

    // Manejar el botón para ataque de desautenticación
    document.getElementById("deauthAttackButton").addEventListener("click", async () => {
        const interface = interfaceSelect.value;

        // Validar que se seleccione una interfaz
        if (!interface) {
            handleError("Interfaz no proporcionada. Seleccione una interfaz antes de continuar.");
            return;
        }

        // Pedir el BSSID del AP
        const bssid = prompt("Ingrese el BSSID del AP:");
        if (!bssid) {
            handleError("BSSID no proporcionado.");
            return;
        }

        // Pedir la dirección MAC del cliente (opcional)
        const client_mac = prompt("Ingrese la MAC del cliente (opcional):");

        // Crear el cuerpo de la solicitud
        const data = {
            interface,
            bssid,
            client_mac: client_mac || null, // Asegurarse de que sea null si no se proporciona
        };

        // Enviar la solicitud al servidor
        const response = await postRequest("/deauth_attack", data);

        // Manejar la respuesta del servidor
        if (response) {
            if (response.error) {
                handleError(response.error);
            } else {
                resultDiv.innerHTML = `<pre>${JSON.stringify(response, null, 2)}</pre>`;
        }
        } else {
            handleError("Error al comunicarse con el servidor.");
        }
    });
});