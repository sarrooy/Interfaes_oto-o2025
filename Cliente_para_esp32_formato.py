import requests
# NOTA: Debes instalar la librería 'requests' si no la tienes: pip install requests

# Configura la dirección IP del ESP32 y el puerto
HOST = "192.168.66.84" # Reemplaza con la IP real del ESP32
PORT = 80
# La URL base para el servidor web
URL_BASE = f"http://{HOST}:{PORT}/"

def enviar_comando_esp32(comando):
    """
    Envía una solicitud HTTP GET al ESP32 con el comando en el parámetro 'mensaje'.
    """
    try:
        # Define los parámetros de la solicitud (el 'mensaje' que espera el ESP32)
        parametros = {'mensaje': comando}
        
        # Realiza la solicitud HTTP GET
        print(f"Enviando solicitud GET a: {URL_BASE}?mensaje={comando}")
        respuesta = requests.get(URL_BASE, params=parametros, timeout=5)
        
        # Comprueba si la solicitud fue exitosa (código de estado 200)
        if respuesta.status_code == 200:
            print(f"Comando enviado: {comando}")
            print(f"Recibido (Respuesta HTTP): {respuesta.text.strip()}")
        else:
            print(f"Error al conectar o recibir respuesta (Código de estado: {respuesta.status_code})")
            print(f"Respuesta del servidor: {respuesta.text.strip()}")

    except requests.exceptions.ConnectionError:
        print("NO se pudo conectar. Asegúrate de que el ESP32 esté encendido, conectado a la misma red y en modo servidor.")
    except requests.exceptions.Timeout:
        print("Tiempo de espera agotado. El ESP32 no respondió a tiempo.")
    except Exception as e:
        print(f"Error inesperado: {e}")

# --- Ejemplo de uso ---
# Solicitar al usuario el comando a enviar
# palabra = input('Escribe lo que deseas enviarle al ESP32 (ej. ON, OFF, hola, Analogica): ')
# enviar_comando_esp32(palabra)

# Ejemplo de envío del comando "ON"
enviar_comando_esp32("ON")

# Puedes probar otros comandos:
# enviar_comando_esp32("OFF")
# enviar_comando_esp32("hola")
# enviar_comando_esp32("Analogica")