from locust import HttpUser, task, between
import random

class FlaskAPIUser(HttpUser):
    wait_time = between(1, 3)  # Tiempo de espera entre tareas (en segundos)

    # Prueba de carga para el endpoint /ping
    @task
    def ping(self):
        self.client.get("/ping")

    # Prueba de carga para el endpoint /tweet
    @task
    def tweet(self):
        # Mensajes SMS de prueba
        test_messages = [
            "Alerta de fraude en Bancolombia",
            "Mensaje de seguridad de Davivienda",
            "Notificación de BBVA",
            "Fraude en Banco de Bogotá",
            "Información del banco popular",
        ]
        sms_message = random.choice(test_messages)  # Selecciona un mensaje aleatorio

        # Enviar una solicitud POST a /tweet
        self.client.post(
            "/tweet",
            json={"sms": sms_message},
            headers={"Content-Type": "application/json"}
        )
