import cv2
import numpy as np
import pyautogui
import socket
import pickle
import struct

# Configuración del servidor
server_ip = "0.0.0.0"  # Escucha en todas las interfaces de red
server_port = 8080      # Puerto en el que el cliente va a recibir las conexiones

# Dirección del cliente (se conecta al cliente mediante su IP)
client_ip = input("Introduce la IP del cliente: ")  # IP del cliente
client_port = 8080  # Puerto en el que el cliente está escuchando
client_address = (client_ip, client_port)

# Crear socket para conexión con el cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(client_address)  # Conectar al cliente

print(f"Conectado al cliente en {client_ip}:{client_port}")

# Establecer la tasa de actualización del video
fps = 30  # Frames por segundo

while True:
    # Capturar la pantalla
    screenshot = pyautogui.screenshot()

    # Convertir la captura de pantalla a un arreglo NumPy (para OpenCV)
    frame = np.array(screenshot)

    # Convertir de RGB (de PyAutoGUI) a BGR (de OpenCV)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Comprimir la imagen para enviarla
    data = pickle.dumps(frame)
    message_size = struct.pack("L", len(data))  # Empaque el tamaño del mensaje

    # Enviar el tamaño del mensaje y los datos al cliente
    client_socket.sendall(message_size + data)

    # Control de la tasa de frames (frames por segundo)
    cv2.waitKey(int(1000 / fps))  # Espera para controlar la tasa de fps

# Cerrar la conexión después de finalizar
client_socket.close()
