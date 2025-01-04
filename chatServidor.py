import socket
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

# Tema de colores en tonos azules
bg_color = "#d8eefe"  # Fondo general azul claro
fg_color = "#002f6c"  # Texto azul oscuro
entry_bg = "#ffffff"  # Fondo de entrada blanco
btn_bg = "#007bff"    # Botones azul vibrante
btn_hover = "#0056b3" # Botones al pasar el mouse en azul más oscuro
btn_fg = "#ffffff"    # Texto de los botones en blanco

def iniciar_servidor():
    global conexion, servidor
    host = "0.0.0.0"
    puerto = 12456

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, puerto))
    servidor.listen(1)
    actualizar_texto("Servidor escuchando...")

    conexion, direccion = servidor.accept()
    actualizar_texto(f"Conexión establecida con {direccion}")

    # Iniciar hilo para recibir mensajes
    hilo_recibir = threading.Thread(target=recibir_mensajes)
    hilo_recibir.start()

def recibir_mensajes():
    while True:
        try:
            mensaje = conexion.recv(1024).decode('utf-8')
            if mensaje.lower() == "salir":
                actualizar_texto("El cliente se desconectó.")
                break
            actualizar_texto(f"Cliente: {mensaje}")
        except:
            actualizar_texto("Error al recibir mensaje.")
            break

def enviar_mensaje():
    mensaje = entrada_mensaje.get()
    conexion.send(mensaje.encode('utf-8'))  # Enviar mensaje al cliente
    actualizar_texto(f"Tú: {mensaje}")
    entrada_mensaje.delete(0, tk.END)
    if mensaje.lower() == "salir":
        servidor.close()
        root.destroy()

def actualizar_texto(mensaje):
    texto.config(state=tk.NORMAL)
    texto.insert(tk.END, mensaje + "\n")
    texto.config(state=tk.DISABLED)

def limpiar_chat():
    texto.config(state=tk.NORMAL)
    texto.delete(1.0, tk.END)
    texto.config(state=tk.DISABLED)

def regresar_menu():
    try:
        servidor.close()
    except:
        pass
    root.destroy()

# Interfaz gráfica
root = tk.Tk()
root.title("Servidor Chat")
root.configure(bg=bg_color)

texto = ScrolledText(root, state=tk.DISABLED, width=50, height=20, bg=entry_bg, fg=fg_color, font=("Arial", 12))
texto.pack(padx=10, pady=10)

frame_mensajes = tk.Frame(root, bg=bg_color)
frame_mensajes.pack()

entrada_mensaje = tk.Entry(frame_mensajes, width=40, bg=entry_bg, fg=fg_color, font=("Arial", 12))
entrada_mensaje.pack(side=tk.LEFT, padx=5)

boton_enviar = tk.Button(frame_mensajes, text="Enviar", command=enviar_mensaje, bg=btn_bg, fg=btn_fg, font=("Arial", 12))
boton_enviar.pack(side=tk.LEFT, padx=5)

boton_iniciar = tk.Button(root, text="Iniciar Servidor", command=iniciar_servidor, bg=btn_bg, fg=btn_fg, font=("Arial", 12))
boton_iniciar.pack(pady=10)

boton_limpiar = tk.Button(root, text="Limpiar Chat", command=limpiar_chat, bg=btn_bg, fg=btn_fg, font=("Arial", 12))
boton_limpiar.pack(pady=5)

boton_menu = tk.Button(root, text="Regresar al Menú", command=regresar_menu, bg=btn_bg, fg=btn_fg, font=("Arial", 12))
boton_menu.pack(pady=5)

# Estilos de hover para botones
def on_enter(event, boton):
    boton['bg'] = btn_hover

def on_leave(event, boton):
    boton['bg'] = btn_bg

# Asociar eventos de hover
for boton in [boton_enviar, boton_iniciar, boton_limpiar, boton_menu]:
    boton.bind("<Enter>", lambda event, boton=boton: on_enter(event, boton))
    boton.bind("<Leave>", lambda event, boton=boton: on_leave(event, boton))

root.mainloop()
