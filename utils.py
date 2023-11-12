import sqlite3
import paho.mqtt.client as mqtt


def mqtt_connect():
    server_address = "h571be95.ala.us-east-1.emqxsl.com"
    mqtt_port = 8883
    ca_cert = "static/cert/emqxsl-ca.crt"
    username = "test"
    password = "test"

    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(username, password)
    mqtt_client.tls_set(ca_cert)
    try:
        mqtt_client.connect(server_address, mqtt_port, 60)

        def on_message(client, userdata, message):
            payload = str(message.payload.decode('utf-8'))
            print(f"Mensaje recibido '{payload}' en el tópico '{message.topic}'")

        mqtt_client.on_message = on_message
        mqtt_client.loop_start()
        return mqtt_client

    except Exception as e:
        print('Se ha producido un error al conectar al servidor MQTT:', str(e))


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
