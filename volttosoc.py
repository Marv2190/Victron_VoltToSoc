# Dieses Script versucht die SOC an die Gegebenheit(Volt) der Akkus anzupassen
import time
import paho.mqtt.client as mqtt
import datetime
import logging
import json

verbunden = 0
cerboserial = "123456789"    # Ist auch gleich VRM Portal ID
broker_address = "192.168.1.xxx"

akkuvolt = 0
akkupro = 0
dcpower = 0
m = 1
setakkuto = '{"value": 32}'

logging.basicConfig(filename='Error.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

def on_disconnect(client, userdata, rc):
    global verbunden
    print("Client Got Disconnected")
    if rc != 0:
        print('Unexpected MQTT disconnection. Will auto-reconnect')

    else:
        print('rc value:' + str(rc))

    try:
        print("Trying to Reconnect")
        client.connect(broker_address)
        verbunden = 1
    except Exception as e:
        logging.exception("Fehler beim reconnecten mit Broker")
        print("Error in Retrying to Connect with Broker")
        verbunden = 0
        print(e)

def on_connect(client, userdata, flags, rc):
        global verbunden
        if rc == 0:
            print("Connected to MQTT Broker!")
            verbunden = 1
            client.subscribe("N/" + cerboserial + "/vebus/276/Soc")
            client.subscribe("N/" + cerboserial + "/vebus/276/Dc/0/Voltage")
            client.subscribe("N/" + cerboserial + "/system/0/Dc/Battery/Power")
        else:
            print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, msg):
    try:

        global akkuvolt, dcpower, akkupro
        # print(msg.topic+" "+str(msg.payload))
        if msg.topic == "N/" + cerboserial + "/vebus/276/Dc/0/Voltage":   # Akku Spannung

            akkuvolt = json.loads(msg.payload)
            akkuvolt = round(float(akkuvolt['value']), 2)

        if msg.topic == "N/" + cerboserial + "/system/0/Dc/Battery/Power":   # Akku Watt Nutzung

            dcpower = json.loads(msg.payload)
            dcpower = int(dcpower['value'])

        if msg.topic == "N/" + cerboserial + "/vebus/276/Soc":   # Akkuprozent

            akkupro = json.loads(msg.payload)
            akkupro = int(akkupro['value'])

    except Exception as e:
        print(e)
        print("Im VTS Programm ist etwas beim auslesen der Nachrichten schief gegangen")

# Konfiguration MQTT
client = mqtt.Client("volttosoc")  # create new instance
client.on_disconnect = on_disconnect
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address)  # connect to broker

logging.debug("Programm Volt to SOC wurde gestartet")

client.loop_start()
time.sleep(1)
print(setakkuto)
while (1):
    m = 1+m
    print(str(akkuvolt)+"V " + str(dcpower) + "W " + str(akkupro) + "% " + str(m))

    # Wenn SOC über 32% aber Spannung unter 52V gesunken und Akkubelastung unter 200W, setze SOC auf 30
    if akkupro > 33 and akkuvolt < 52 and dcpower < 200 and dcpower > -200:
        print("Akku über 33% und Spannung unter 52V! Setze Akku auf 32%")
        try:
            client.publish("W/" + cerboserial + "/vebus/276/Soc", setakkuto)
        except Exception as e:
            print(e)
    else:
        print("Akkuprozent ist nicht über 33% und Spannung unter 52V während unter 200W Belastung bestehen")
    time.sleep(3600)