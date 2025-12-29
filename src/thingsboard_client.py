import paho.mqtt.client as mqtt
import json
import time

# === CONFIGURE ICI TES INFOS THINGSBOARD ===
THINGSBOARD_HOST = "demo.thingsboard.io" 
ACCESS_TOKEN = "Smc41S74DCYXGpYPAWdn"
client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connecté à ThingsBoard !")
        else:
            print(f"Échec connexion, code {rc}")

    client.on_connect = on_connect
    client.connect(THINGSBOARD_HOST, 1883, 60)
    client.loop_start()  # Démarre la boucle en fond

def send_telemetry(status: str, score: float):
    """
    Envoie le statut et le score à ThingsBoard
    """
    payload = {
        "status": status,      # "OK" ou "KO"
        "anomaly_score": round(score, 4)
    }
    client.publish("v1/devices/me/telemetry", json.dumps(payload))
    print(f"Télémetry envoyée : {payload}")
    time.sleep(1)  # Petit délai pour éviter les floods

# Connexion au démarrage
connect_mqtt()