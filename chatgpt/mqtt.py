import paho.mqtt.client as mqtt
import ssl


def connect_mqtt():
    server_address = "h571be95.ala.us-east-1.emqxsl.com"
    mqtt_port = 8883
    ca_cert = "cert/emqxsl-ca.crt"  # Reemplaza "ruta_al_ca_certificate.pem" por la ubicación de tu archivo CA Certificate
    username = "test"
    password = "test"  # Si es necesario

    # Callback para cuando se establece la conexión
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Conexión exitosa")

        else:
            print("Error de conexión, código de retorno: " + str(rc))

    # Crear un cliente MQTT
    client = mqtt.Client()
    # Configurar la conexión con TLS/SSL y el CA Certificate
    client.tls_set(ca_certs=ca_cert, certfile=None, keyfile=None, cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLS)

    # Configurar nombre de usuario y contraseña (si es necesario)
    client.username_pw_set(username, password)

    # Configurar los callbacks
    client.on_connect = on_connect

    # Conectar al servidor MQTT
    client.connect(server_address, mqtt_port, 60)
    client.publish('test', 'test')

    # Iniciar el bucle para mantener la conexión
    client.loop_forever()
