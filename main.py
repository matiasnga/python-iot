import json
import time

from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt
import ssl

app = Flask(__name__)

# Configura la información de conexión MQTT
server_address = "h571be95.ala.us-east-1.emqxsl.com"
mqtt_port = 8883
ca_cert = "cert/emqxsl-ca.crt"
username = "test"
password = "test"
received_messages = []
topic = 'test'


# Callback cuando se recibe un mensaje MQTT
def on_message(client, userdata, message):
    global json_data
    message_data = message.payload.decode()
    try:
        json_data = json.loads(message_data)
        print(json_data)
    except json.JSONDecodeError:
        pass


# Inicializa el cliente MQTT
mqtt_client = mqtt.Client()
mqtt_client.tls_set(ca_certs=ca_cert, certfile=None, keyfile=None, cert_reqs=ssl.CERT_NONE,
                    tls_version=ssl.PROTOCOL_TLS)
mqtt_client.username_pw_set(username, password)
mqtt_client.on_message = on_message
mqtt_client.connect(server_address, mqtt_port, 60)


# Función para enviar un mensaje al tópico
def send_message(message):
    mqtt_client.publish(topic, message)


# Función que envía mensajes cada 1 segundo en un hilo separado


def send_set_temp(temperature):
    set_temp_message = {"setTemp": temperature}
    print(set_temp_message)
    send_message(json.dumps(set_temp_message))


# Ruta para la página web
@app.route('/')
def index():
    test_message = {
        "temp": 25,
        "fecha": "2023-11-08 10:00:00",
        "caldera_encendida": True
    }
    send_message(json.dumps(test_message))
    return render_template('base.html', messages=test_message)


@app.route('/get_latest_temperature', methods=['GET'])
def get_latest_temperature():
    global latest_temperature
    return str('50')


# Ruta para obtener mensajes en formato JSON
@app.route('/get_messages', methods=['GET'])
def get_messages():
    start = int(request.args.get('start', 0))
    messages = received_messages[start:]
    return jsonify(messages)


if __name__ == "__main__":
    mqtt_client.subscribe(topic)
    mqtt_client.loop_start()
    # Enviar un mensaje JSON de prueba al tópico cuando se inicie el programa


    app.run(debug=True, host='0.0.0.0')
