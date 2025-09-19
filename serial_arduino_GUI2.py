import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
import time

# --- Variables Globales ---
is_connected = False
reading_active = False
arduino = None
update_interval_ms = 100 # Frecuencia de muestreo (refresco) en milisegundos

# --- Configuración de datos para la gráfica ---
max_puntos = 100  # Puntos a mostrar en la gráfica
datosY = deque([0] * max_puntos, maxlen=max_puntos)
datosX = deque(range(max_puntos), maxlen=max_puntos)

# --- Funciones de la Aplicación ---

def find_serial_ports():
    """Encuentra y devuelve una lista de puertos COM disponibles."""
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def toggle_connection():
    """Conecta o desconecta del puerto serie."""
    global is_connected, arduino, reading_active

    if not is_connected:
        try:
            port = combo_ports.get()
            baudrate = int(combo_baud.get())
            if not port:
                messagebox.showerror("Error", "Por favor, selecciona un puerto COM.")
                return

            arduino = serial.Serial(port=port, baudrate=baudrate, timeout=0.1)
            print(f"Conectado a {arduino.port} a {arduino.baudrate} baudios.")
            
            # Actualizar estado de la GUI
            is_connected = True
            reading_active = True
            status_label.config(text="Conectado", fg="green")
            connect_button.config(text="Desconectar")
            combo_ports.config(state="disabled")
            combo_baud.config(state="disabled")
            
            # Iniciar la lectura de datos
            leer_datos_serial()

        except serial.SerialException as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar al puerto {port}.\nCausa: {e}")
            if arduino:
                arduino.close()
            is_connected = False
            reading_active = False
    else:
        # Desconectar
        reading_active = False
        if arduino and arduino.is_open:
            arduino.close()
            print("Conexión a puerto serie cerrada.")
        
        is_connected = False
        status_label.config(text="Desconectado", fg="red")
        connect_button.config(text="Conectar")
        combo_ports.config(state="readonly")
        combo_baud.config(state="readonly")


def leer_datos_serial():
    """Lee datos del puerto serie y actualiza la gráfica."""
    global arduino, reading_active

    if reading_active and arduino and arduino.in_waiting > 0:
        try:
            linea_leida = arduino.readline().decode('utf-8').strip()
            if linea_leida:
                valor = int(linea_leida)
                print(f"ADC: {valor}")
                actualizar_grafica(valor)
        except (ValueError, UnicodeDecodeError):
            print(f"Dato no válido recibido: {linea_leida}")

    # Programar la próxima lectura si seguimos activos
    if reading_active:
        ventana.after(update_interval_ms, leer_datos_serial)


def actualizar_grafica(valor):
    """Actualiza los datos y redibuja la gráfica."""
    datosY.append(valor)
    linea.set_ydata(datosY)
    
    # Redibujar el canvas
    canvas.draw()
    canvas.flush_events()

def on_closing():
    """Maneja el cierre de la ventana para desconectar el puerto."""
    global reading_active
    if is_connected:
        reading_active = False
        time.sleep(0.2) # Pequeña pausa para que el bucle `after` se detenga
        if arduino and arduino.is_open:
            arduino.close()
            print("Puerto serie cerrado al salir.")
    ventana.destroy()

# --- Creación de la Ventana Principal (GUI) ---
ventana = tk.Tk()
ventana.title("Interfaz Gráfica Serial Arduino")
ventana.geometry("800x600")

# --- Creación del Notebook (Pestañas) ---
nb = ttk.Notebook(ventana)
nb.pack(fill='both', expand=True, padx=10, pady=10)

# --- Pestaña 1: Conexión ---
p1_conexion = ttk.Frame(nb)
nb.add(p1_conexion, text="Configuración de Conexión")

conexion_frame = ttk.LabelFrame(p1_conexion, text="Parámetros de Conexión")
conexion_frame.pack(padx=20, pady=20, fill="x")

# Widgets para seleccionar puerto COM
label_ports = ttk.Label(conexion_frame, text="Puerto COM:")
label_ports.grid(row=0, column=0, padx=5, pady=10, sticky="w")
combo_ports = ttk.Combobox(conexion_frame, state="readonly", values=find_serial_ports())
combo_ports.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

# Widgets para seleccionar Baudrate
label_baud = ttk.Label(conexion_frame, text="Baudrate:")
label_baud.grid(row=1, column=0, padx=5, pady=10, sticky="w")
common_baudrates = [9600, 19200, 38400, 57600, 115200]
combo_baud = ttk.Combobox(conexion_frame, state="readonly", values=common_baudrates)
combo_baud.set(19200) # Valor por defecto
combo_baud.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

# Botón para conectar/desconectar
connect_button = ttk.Button(p1_conexion, text="Conectar", command=toggle_connection)
connect_button.pack(pady=15)

# Label para mostrar el estado de la conexión
status_label = ttk.Label(p1_conexion, text="Desconectado", font=("Helvetica", 12, "bold"), foreground="red")
status_label.pack(pady=10)


# --- Pestaña 2: Gráfica ---
p2_grafica = ttk.Frame(nb)
nb.add(p2_grafica, text="Gráfica en Tiempo Real")

# Configuración de la figura de Matplotlib
fig, ax = plt.subplots(facecolor='#F0F0F0') # Mismo color de fondo que Tkinter
linea, = ax.plot(datosX, datosY)
ax.set_title('Gráfica de Conversión ADC')
ax.set_xlabel('Muestras')
ax.set_ylabel('Valor del Sensor (ADC)')
ax.set_ylim(0, 1024)
ax.set_xlim(0, max_puntos)
ax.grid(True)

# Incrustar la gráfica en la ventana de Tkinter
canvas = FigureCanvasTkAgg(fig, master=p2_grafica)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Texto con la frecuencia de muestreo
refresh_label = ttk.Label(p2_grafica, text=f"Frecuencia de refresco: {update_interval_ms} ms")
refresh_label.pack(pady=5)


# --- Bucle Principal de la Aplicación ---
ventana.protocol("WM_DELETE_WINDOW", on_closing) # Asignar función de cierre seguro
ventana.mainloop()