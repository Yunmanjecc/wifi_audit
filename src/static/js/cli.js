document.addEventListener("DOMContentLoaded", () => {
    const commandInput = document.getElementById("cliCommand");
    const executeButton = document.getElementById("executeCommand");
    const outputPre = document.querySelector("#cliOutput pre");

    // Función para ejecutar comandos
    async function executeCommand(command) {
        try {
            const response = await fetch("/execute_command", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ command }),
            });

            if (!response.ok) {
                throw new Error(`Error al ejecutar el comando: ${response.statusText}`);
            }

            const result = await response.json();
            outputPre.textContent = result.output || "Comando ejecutado sin salida.";
        } catch (error) {
            outputPre.textContent = `Error: ${error.message}`;
        }
    }

    // Ejecutar comando al hacer clic en el botón
    executeButton.addEventListener("click", () => {
        const command = commandInput.value.trim();
        if (!command) {
            outputPre.textContent = "Error: Ingresa un comando válido.";
            return;
        }
        executeCommand(command);
    });
});
