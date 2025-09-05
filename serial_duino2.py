import serial 
import matplotlib.pyplot as plt
# es una biblioteca para coleccion de datos a graficar
from collections import deque
import time 

#configuracion de parametros de la grafica
max_puntos = 100 #puntos a mostrar en la grafica
datosY = deque([0] * max_puntos)
datosX = deque(range(max_puntos))

#configuracion de grafia en tiempo real 
fig, ax = plt.subplots()
linea, =  ax.plot(datosX, datosY)
plt.title('Gracida de conversion ADC')
plt.xlabel('Tiempo')
plt.ylabel('Valor del Sensor (ADC)')
ax.set_ylim(0, 4096) #ajuste de datos para 12bits
plt.grid(True)

# def funcion para actualizar Grafia de forma continua
def actualizar_grafica(valor):
    #metodo que atulizaria el dato uno a uno y se va recorriendo la informacion
    datosY.popleft() #esto es para recorrer la grafica a medida que avanza el time
    datosY.append(valor) #con esto se apilan los datos Concatenando
    linea.set_ydata(datosY)
    fig.canvas.draw()
    fig.canvas.flush_events()

#bloque try para realiza la conexion a COM4
try:
    arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1) 
    print(f"conectados a {arduino.port} a baudios = {arduino.baudrate}")
except serial.SerialException as e:
    print("Error de conexion; causa: {e}")
    exit()

#bucle principal de graficacion
try:
    #Activamos o instanciamos mostrar la grafica 	
    plt.ion()
    plt.show()
    while True:
        print("entramos al while TRUE")
        if arduino.in_waiting > 0:
            print("leemos dato")
            linea_leida = arduino.readline().decode('utf-8').strip()
            try:
                valor = float(linea_leida)
                print(f"ADC: {valor}")
                actualizar_grafica(valor)
            except ValueError:
                print(f"Error de dato:{linea_leida}")
        else:
                print("no se encotro dato")
    time.sleep(0.01)	
 
except KeyboardInterrupt:
	print("programa finalizado por el usuario")
        
finally:
    if 'arduino' in locals() and arduino.is_open:
        arduino.close()
        print("conexion a puerto serie Cerrada")