let touchStartY = 0;
let touchEndY = 0;
const threshold = 150; // Umbral para el deslizamiento

window.addEventListener('touchstart', function(event) {
    touchStartY = event.changedTouches[0].screenY;
}, false);

window.addEventListener('touchmove', function(event) {
    touchEndY = event.changedTouches[0].screenY;
    if (touchStartY < touchEndY && (touchEndY - touchStartY) > threshold) {
        // Mostrar el indicador de refresco
        document.getElementById('refresh-indicator').style.display = 'block';
    }
}, false);
window.addEventListener('touchend', function(event) {
    if (touchStartY < touchEndY && (touchEndY - touchStartY) > threshold) {
        var refreshIndicator = document.getElementById('refresh-indicator');
        refreshIndicator.classList.add('visible'); // Mostrar el spinner

        setTimeout(function() {
            // Ocultar el spinner después de un tiempo
            refreshIndicator.classList.remove('visible');
            location.reload(); // Recargar la página
        }, 500); // Ajusta este tiempo según sea necesario
    }
}, false);
