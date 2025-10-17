#include <WiFi.h>
#include <WebServer.h>

// Sustituye con tus credenciales de red
//const char* ssid = "BUAP_Estudiantes";
//const char* password = "f85ac21de4";
const char* ssid = "UPPue-WiFi";
const char* password = NULL;
// Crea un objeto servidor web en el puerto 80 (el puerto HTTP por defecto)
WebServer server(80);

void setup() {
 Serial.begin(115200);
 // Conecta el ESP32 a la red WiFi
 WiFi.begin(ssid, password);
 while (WiFi.status() != WL_CONNECTED) {
   delay(500);
   Serial.println("Conectando a la red WiFi...");
 }
 Serial.println("Conectado a la red WiFi.");
 Serial.print("Dirección IP del servidor: ");
 Serial.println(WiFi.localIP());
 // Define la función a ejecutar cuando el servidor recibe una solicitud en la ruta raíz "/"
 server.on("/", handleRoot);
 // Inicia el servidor
 server.begin();
 Serial.println("Servidor HTTP iniciado.");

 pinMode(2, OUTPUT);
}

void loop() {
 // Maneja las solicitudes de los clientes de forma continua
 server.handleClient();
}

void handleRoot() {
 // Comprueba si la solicitud del cliente es una solicitud GET
 server.send(200, "text/plain", "no haces esto 1");
 if (server.method() == HTTP_GET) {
   // Obtiene la cadena de la solicitud GET (ej. http://<IP_ESP32>/?mensaje=hola)
   String mensaje = server.arg("mensaje");
   // Imprime el mensaje recibido en el monitor serial
   Serial.print("Mensaje recibido: ");
   Serial.println(mensaje);
   server.send(200, "text/plain", "Mensaje recibido: ");
   // Comprueba si el mensaje recibido es "hola"
   if (mensaje == "hola") {
     // Si el mensaje es "hola", responde con un número aleatorio
     int numeroAleatorio = random(1, 100); // Genera un número entre 1 y 99
     String respuesta = String(numeroAleatorio);
     server.send(200, "text/plain", respuesta);
     Serial.print("Respondiendo con el número: ");
     Serial.println(respuesta);
   }
    else if (mensaje == "ON"){
      String respuesta = "ON";
     server.send(200, "text/plain", respuesta);
     Serial.print("Respondiendo con el número: ");
     Serial.println(respuesta);
     digitalWrite(2, HIGH);
    }
    else if (mensaje == "OFF"){
      String respuesta = "OFF";
     server.send(200, "text/plain", respuesta);
     Serial.print("Respondiendo con el número: ");
     Serial.println(respuesta);
     digitalWrite(2, LOW);
    }
    else if (mensaje == "Analogica"){
      int datoAnalogico = analogRead(36);
      String respuesta = String(datoAnalogico);
     server.send(200, "text/plain", respuesta);
     Serial.print("Respondiendo con el número: ");
     Serial.println(datoAnalogico);
     
    }
    else {
     // Si el mensaje no es "hola", envía una respuesta predeterminada
     server.send(200, "text/plain", "Mensaje no reconocido.");
   }
 }
}