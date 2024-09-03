import random
import time
import paho.mqtt.client as mqtt

# Função para simular leitura de energia
def simular_consumo_energia():
    return round(random.uniform(50, 500) + random.gauss(0, 10), 2)  # Adiciona um pouco de ruído

# Configuração MQTT
broker = "test.mosquitto.org"  # Servidor MQTT público para testes
topico = "energia/consumo"

client = mqtt.Client("Sensor_Energia", protocol=mqtt.MQTTv311)
client.connect(broker)

# Loop de envio de dados
try:
    while True:
        consumo = simular_consumo_energia()
        client.publish(topico, consumo)
        print(f"Consumo enviado: {consumo} Watts")
        time.sleep(5)  # Envia dados a cada 5 segundos
except KeyboardInterrupt:
    print("Emulação interrompida")
    client.disconnect()
