var mqttClient; // Inicializa tu cliente MQTT aquí o asegúrate de que esté disponible globalmente

document.addEventListener('mqttConnected', function(event) {
    mqttClient = event.detail; // Asegúrate de que mqttClient está disponible en el scope global
    var topic = "16092021/#";
    mqttClient.subscribe(topic);
    console.log('Suscrito a los topics después de la conexión MQTT');
    mqttClient.on('message', (topic, message) => {
        console.log(topic + '-> ' + message.toString());
        if (topic === '16092021/temp') {
            document.getElementById('current-temp-mqtt').innerText = message.toString() + '° C';
        }
        if (topic === '16092021/status_temp') {
            var btn = 'btn-emisor-mqtt'
            var emisorIsOnline = (message.toString() === 'online');
            updateStatusDisplay(emisorIsOnline, btn);
        }

        if (topic === '16092021/status_relay') {
            var btn = 'btn-receptor-mqtt'
            var receptorIsOnline = (message.toString() === 'online');
            updateStatusDisplay(receptorIsOnline, btn);
        }

        if (topic === '16092021/relay') {
            var btn = 'btn-caldera-mqtt'

            var calderaIsOn = ((message.toString() === 'on') );
            updateStatusDisplay(calderaIsOn, btn);
        }

         if (topic === '16092021/settemp') {
            setTemperature = message.toString();
            document.getElementById('target-temp').innerText = setTemperature + '° C';
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Eventos de clic para botones de temperatura
    document.getElementById('increaseTemp').addEventListener('click', function() {
        sendTemperatureChange(1);
    });

    document.getElementById('decreaseTemp').addEventListener('click', function() {
        sendTemperatureChange(-1);
    });
});

function sendTemperatureChange(delta) {

    var currentTemp = parseInt(document.getElementById('target-temp').innerText);
    var newTemp = currentTemp + delta;
    mqttClient.publish('16092021/settemp', newTemp.toString(), {retain: true }
    );
}

function updateStatusDisplay(isOnline, btn) {
    var btn = document.getElementById(btn);
    if (btn) {
        if (isOnline) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    }
}
