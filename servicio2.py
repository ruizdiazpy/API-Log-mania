import requests
import json
import time
from datetime import datetime

TOKEN = 'token_servicio2'

def generar_log():
    log = {
        "fecha_hora": datetime.now().isoformat(),
        "nombre_servicio": "servicio2",
        "nivel_severidad": "Error",
        "mensaje": "Log de prueba servicio 2"
    }
    return log

def enviar_log():
    url = "http://localhost:5000/logs"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }
    log = generar_log()
    response = requests.post(url, headers=headers, data=json.dumps(log))
    print(response.status_code, response.text)

if __name__ == "__main__":
    while True:
        enviar_log()
        time.sleep(5)
