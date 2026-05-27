setTimeout(() => {
    const textoPagina = document.body.innerText.toLowerCase();
    const palabrasClave = ["términos y condiciones", "política de privacidad", "terms of service", "privacy policy"];
    
    const contieneLegal = palabrasClave.some(palabra => textoPagina.includes(palabra));

    if (contieneLegal) {
        crearPanelUI();
        analizarTexto();
    }
}, 2000);

function crearPanelUI() {
    const panel = document.createElement('div');
    panel.id = 'privascanner-panel';
    panel.innerHTML = `
        <div class="header">
            <h3>PrivaScanner</h3>
            <button id="privascanner-close">✖</button>
        </div>
        <div id="privascanner-content">
            <p>Procesando documento con NLP...</p>
        </div>
    `;
    document.body.appendChild(panel);

    document.getElementById('privascanner-close').addEventListener('click', () => {
        panel.remove();
    });
}

async function analizarTexto() {
    // Extraer texto visible
    const textoVisible = document.body.innerText.substring(0, 10000);

    chrome.runtime.sendMessage(
        { action: "analizarTexto", texto: textoVisible },
        (response) => {
            if (response && response.success) {
                mostrarResultados(response.data.resultado);
            } else {
                let errMsg = response && response.error ? response.error : "Error desconocido";
                mostrarResultados(`Error al analizar el documento.<br><br><b>Detalle:</b> ${errMsg}<br><br>Asegúrate de que el servidor esté en ejecución y la API Key esté configurada.`);
                console.error("Error desde background:", errMsg);
            }
        }
    );
}

function mostrarResultados(markdownText) {
    const contenedor = document.getElementById('privascanner-content');
    
    // Formateo básico de Markdown a HTML
    let htmlFormateado = markdownText
        .replace(/### (.*?)\n/g, '<h4>$1</h4>') // Cabeceras
        .replace(/\n/g, '<br>') // Saltos de línea
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Negritas
        .replace(/\* (.*?)(<br>|$)/g, '<li>$1</li>'); // Listas
        
    contenedor.innerHTML = htmlFormateado;
}
