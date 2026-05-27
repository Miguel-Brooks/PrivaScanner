chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "analizarTexto") {
        fetch('http://localhost:8000/analizar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ texto: request.texto })
        })
        .then(async (response) => {
            if (!response.ok) {
                let errorDetalle = "Error del servidor";
                try {
                    const errJson = await response.json();
                    errorDetalle = errJson.detail || errorDetalle;
                } catch(e) {}
                throw new Error(errorDetalle);
            }
            return response.json();
        })
        .then(data => sendResponse({ success: true, data: data }))
        .catch(error => sendResponse({ success: false, error: error.message }));
        
        return true; // Indica que la respuesta será asíncrona
    }
});
