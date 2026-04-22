document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('graficoCanvas');
    if (!canvas) return;

    let rawData = [];
    try {
        // Obtenemos el objeto completo y extraemos la lista de publicaciones
        const sourceData = JSON.parse(canvas.getAttribute('data-posts'));
        rawData = sourceData.publicaciones || [];
    } catch (e) {
        console.error("Error al procesar datos:", e);
    }

    if (rawData.length > 0) {
        let counts = { "Positivo": 0, "Negativo": 0, "Neutro": 0 };
        let totalLikes = 0;

        rawData.forEach(p => {
            // Conteo de sentimientos
            const s = p.sentimiento || "Neutro";
            if (counts.hasOwnProperty(s)) counts[s]++;
            
            // Limpieza de likes (maneja strings con comas o null)
            const l = String(p.likes || "0").replace(/[^0-9]/g, '');
            totalLikes += parseInt(l) || 0;
        });

        // Actualizar Likes Promedio en el card superior
        const display = document.getElementById('avgLikesDisplay');
        if (display) {
            display.innerText = Math.round(totalLikes / rawData.length).toLocaleString();
        }

        // Renderizar Gráfico
        new Chart(canvas, {
            type: 'doughnut',
            data: {
                labels: ['Positivo', 'Negativo', 'Neutro'],
                datasets: [{
                    data: [counts["Positivo"], counts["Negativo"], counts["Neutro"]],
                    backgroundColor: ['#2ecc71', '#e74c3c', '#95a5a6'],
                    borderWidth: 2,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom' } },
                cutout: '70%'
            }
        });
    }
});