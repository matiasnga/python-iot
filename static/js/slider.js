document.addEventListener('DOMContentLoaded', () => {
    const slider = document.getElementById('slider');
    const valueDisplay = document.getElementById('value-display');
    const switchEl = document.getElementById('switch');

    slider.oninput = function() {
        valueDisplay.innerText = this.value;
    };

    switchEl.onclick = function() {
        this.classList.toggle('switch-active');
        // Aquí puedes añadir más lógica para el switch
    };
});
