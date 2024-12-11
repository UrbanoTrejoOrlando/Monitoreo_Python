import socket
import os
import tkinter as tk
from tkinter import messagebox
import threading

# Configuración del servidor
HOST = '0.0.0.0'  # Escucha en todas las interfaces
PORT = 65432
SAVE_PATH = '/home/starlord/Documents/'  # Cambia esto a la ruta deseada
os.makedirs(SAVE_PATH, exist_ok=True)  # Crear la carpeta si no existe

# Colores del tema
bg_color = "#d8eefe"  # Fondo general azul claro
fg_color = "#002f6c"  # Texto azul oscuro
entry_bg = "#ffffff"  # Fondo de entrada blanco
btn_bg = "#007bff"    # Botones azul vibrante
btn_hover = "#0056b3" # Botones al pasar el mouse en azul más oscuro
btn_fg = "#ffffff"    # Texto de los botones en blanco

# Función para ejecutar el servidor en un hilo
def start_server():
    try:
        # Crear el socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        text_output.insert(tk.END, f"Servidor escuchando en {HOST}:{PORT}\n")
        text_output.yview(tk.END)
        
        while True:
            conn, addr = server_socket.accept()
            text_output.insert(tk.END, f"Conexión establecida con {addr}\n")
            text_output.yview(tk.END)

            try:
                # Recibir el nombre del archivo
                filename = conn.recv(1024).decode('utf-8')
                text_output.insert(tk.END, f"Recibiendo archivo: {filename}\n")
                text_output.yview(tk.END)
            except UnicodeDecodeError:
                text_output.insert(tk.END, "Error: No se pudo decodificar el nombre del archivo.\n")
                text_output.yview(tk.END)
                conn.close()
                continue

            # Ruta completa del archivo
            full_path = os.path.join(SAVE_PATH, filename)

            try:
                # Crear el archivo
                with open(full_path, 'wb') as f:
                    while True:
                        data = conn.recv(4096)
                        if not data:
                            break
                        f.write(data)
                text_output.insert(tk.END, f"Archivo {filename} recibido exitosamente en {full_path}.\n")
                text_output.yview(tk.END)
            except Exception as e:
                text_output.insert(tk.END, f"Error al guardar el archivo: {e}\n")
                text_output.yview(tk.END)

            conn.close()
    except Exception as e:
        text_output.insert(tk.END, f"Error en el servidor: {e}\n")
        text_output.yview(tk.END)

# Función para iniciar el servidor en un hilo
def run_server_thread():
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

# Función para detener el servidor
def stop_server():
    messagebox.showinfo("Servidor detenido", "El servidor ha sido detenido.")
    root.quit()

# Función para regresar al menú principal
def go_to_main_menu():
    response = messagebox.askyesno("Regresar", "¿Estás seguro de que deseas regresar al menú?")
    if response:
        root.quit()

# Crear la ventana principal
root = tk.Tk()
root.title("Servidor de Archivos")
root.geometry("600x400")
root.configure(bg=bg_color)

# Crear un marco para los botones
frame_buttons = tk.Frame(root, bg=bg_color)
frame_buttons.pack(pady=10)

# Botones de inicio, parada y regreso al menú con estilo
btn_start = tk.Button(frame_buttons, text="Iniciar Servidor", command=run_server_thread, bg=btn_bg, fg=btn_fg, font=("Arial", 12), activebackground=btn_hover)
btn_start.pack(side=tk.LEFT, padx=10)

btn_stop = tk.Button(frame_buttons, text="Detener Servidor", command=stop_server, bg=btn_bg, fg=btn_fg, font=("Arial", 12), activebackground=btn_hover)
btn_stop.pack(side=tk.LEFT, padx=10)

btn_menu = tk.Button(frame_buttons, text="Regresar al Menú", command=go_to_main_menu, bg=btn_bg, fg=btn_fg, font=("Arial", 12), activebackground=btn_hover)
btn_menu.pack(side=tk.LEFT, padx=10)

# Crear un área de texto para mostrar los mensajes del servidor con estilo
text_output = tk.Text(root, wrap=tk.WORD, width=70, height=15, bg="#f0f0f0", fg=fg_color, font=("Arial", 10), bd=0, padx=10, pady=10)
text_output.pack(pady=10)
text_output.config(state=tk.DISABLED)

# Ejecutar la interfaz
root.mainloop()
