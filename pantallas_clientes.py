import cv2
import numpy as np
import socket
import struct
from PIL import ImageGrab
import tkinter as tk
from tkinter import messagebox

def conectar():
    host = entry_ip.get()  # Obtener la IP desde el campo de texto
    puerto = 8080

    # Validar IP
    if not host:
        messagebox.showerror("Error", "Por favor ingrese una dirección IP válida")
        return

    # Crear socket
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((host, puerto))
        print(f"Conectado al servidor {host}:{puerto}")
        transmitir_pantalla(cliente_socket)
    except Exception as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar al servidor: {e}")
        
def transmitir_pantalla(cliente_socket):
    try:
        while True:
            # Capturar la pantalla
            screenshot = ImageGrab.grab()
            frame = np.array(screenshot)  # Convertir a array de NumPy (BGR)

            # Redimensionar para transmitir menos datos
            frame = cv2.resize(frame, (800, 450))
            _, frame_encoded = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])

            # Enviar tamaño del frame primero
            data = frame_encoded.tobytes()
            cliente_socket.sendall(struct.pack("!I", len(data)))
            cliente_socket.sendall(data)
    except KeyboardInterrupt:
        print("Cliente detenido")
    finally:
        cliente_socket.close()

# Crear ventana de la interfaz
ventana = tk.Tk()
ventana.title("Conexión al Servidor")
ventana.geometry("300x150")

# Etiqueta y campo de entrada para la IP
label_ip = tk.Label(ventana, text="Dirección IP del servidor:")
label_ip.pack(pady=10)

entry_ip = tk.Entry(ventana, width=20)
entry_ip.pack(pady=5)

# Botón de conexión
boton_conectar = tk.Button(ventana, text="Conectar", command=conectar)
boton_conectar.pack(pady=10)

# Ejecutar la interfaz
ventana.mainloop()
