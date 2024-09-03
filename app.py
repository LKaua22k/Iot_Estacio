from flask import Flask, render_template, jsonify
import paho.mqtt.client as mqtt
import smtplib
from email.mime.text import MIMEText
from collections import deque
import statistics

app = Flask(__name__)

# Variáveis globais para armazenar dados de consumo
consumo_atual = 0
historico_consumo = deque(maxlen=20)  # Armazena os últimos 20 consumos

# Função chamada quando uma mensagem é recebida no tópico MQTT
def on_message(client, userdata, message):
    global consumo_atual
    try:
        consumo_atual = float(message.payload.decode("utf-8"))
        historico_consumo.append(consumo_atual)
        print(f"Mensagem recebida: {consumo_atual} Watts")
        
        # Verifica se o consumo ultrapassa um limite e envia alerta
        if consumo_atual > 400:
            enviar_alerta(consumo_atual)
    except ValueError as e:
        print(f"Erro ao decodificar a mensagem: {e}")

# Função chamada quando o cliente se conecta ao broker MQTT
def on_connect(client, userdata, flags, rc):
    print(f"Conectado com o código de resultado: {rc}")
    client.subscribe(topico)
    print(f"Inscrito no tópico: {topico}")

# Função para enviar alertas por e-mail
def enviar_alerta(consumo):
    msg = MIMEText(f"Alerta: O consumo de energia foi detectado como {consumo} Watts.")
    msg['Subject'] = 'Alerta de Consumo de Energia'
    msg['From'] = 'estacioprojeto13@gmail.com'
    msg['To'] = 'pabloarj22@gmail.com','lkauan462@gmail.com'  # Coloque aqui o e-mail do destinatário

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('estacioprojeto13@gmail.com', 'gimp iosw fhta uedl')
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
        print(f"Alerta enviado para {msg['To']}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

# Configuração MQTT
broker = "test.mosquitto.org"
topico = "energia/consumo"

client = mqtt.Client("Monitor_Energia", protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker)
client.loop_start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dados_consumo')
def dados_consumo():
    media_consumo = statistics.mean(historico_consumo) if historico_consumo else 0
    return jsonify({
        'consumo_atual': consumo_atual,
        'media_consumo': media_consumo,
        'historico_consumo': list(historico_consumo)
    })

if __name__ == "__main__":
    app.run(debug=True)
