var mqttClient = null;
document.addEventListener('DOMContentLoaded', function() {

        // Configura las opciones del cliente MQTT
  var options = {
        connectTimeout: 4000,
        clientId: 'client-id' + Math.floor(Math.random() * 10000),
        username: 'test',
        password: 'test',
        keepalive: 60,
        clean: true,
      };
        if (!mqttClient) {
       var  mqttClient = mqtt.connect('wss://h571be95.ala.us-east-1.emqxsl.com:8084/mqtt', options);



 mqttClient.on('connect', () => {
        console.log('Conectado al servidor MQTT');
        document.dispatchEvent(new CustomEvent('mqttConnected', { detail: mqttClient }));
            document.getElementById('mqtt-loading-overlay').style.display = 'none';

      });

 mqttClient.on('error', (error) => {
        console.log('Error de conexión MQTT:', error);
      });
}
      })