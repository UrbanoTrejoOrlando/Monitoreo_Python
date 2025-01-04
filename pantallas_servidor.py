import socket
import struct
import cv2
import numpy as np

def servidor():
    host = "0.0.0.0"  # Escuchar en todas las interfaces
    puerto = 8080

    # Crear socket
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind((host, puerto))
    servidor_socket.listen(5)
    print(f"Servidor escuchando en {host}:{puerto}")

    cliente_socket, cliente_direccion = servidor_socket.accept()
    print(f"Cliente conectado desde {cliente_direccion}")

    try:
        while True:
            # Recibir el tamaño del frame
            frame_size_data = cliente_socket.recv(4)
            if not frame_size_data:
                break
            frame_size = struct.unpack("!I", frame_size_data)[0]

            # Recibir el frame
            data = b""
            while len(data) < frame_size:
                packet = cliente_socket.recv(4096)
                if not packet:
                    break
                data += packet

            # Convertir los datos en imagen
            frame = np.frombuffer(data, dtype=np.uint8)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            # Mostrar la imagen
            cv2.imshow("Stream desde cliente", frame)
            if cv2.waitKey(1) == 27:  # Presionar 'Esc' para salir
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cv2.destroyAllWindows()
        cliente_socket.close()
        servidor_socket.close()

if __name__ == "__main__":
    servidor()
