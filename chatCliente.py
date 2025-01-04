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

def conectar_servidor():
    global cliente
    host = entrada_ip.get()
    puerto = int(entrada_puerto.get())

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host, puerto))
    actualizar_texto("Conectado al servidor.")

    hilo = threading.Thread(target=recibir_mensajes)
    hilo.start()

def enviar_mensaje():
    mensaje = entrada_mensaje.get()
    cliente.send(mensaje.encode('utf-8'))
    actualizar_texto(f"Tú: {mensaje}")
    entrada_mensaje.delete(0, tk.END)
    if mensaje.lower() == "salir":
        cliente.close()
        root.destroy()

def recibir_mensajes():
    while True:
        try:
            mensaje = cliente.recv(1024).decode('utf-8')
            actualizar_texto(f"Servidor: {mensaje}")
        except:
            actualizar_texto("Conexión cerrada.")
            break

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
        cliente.close()
    except:
        pass
    root.destroy()

# Interfaz gráfica
root = tk.Tk()
root.title("Cliente Chat")
root.configure(bg=bg_color)

frame_conexion = tk.Frame(root, bg=bg_color)
frame_conexion.pack(pady=10)

tk.Label(frame_conexion, text="IP Servidor:", fg=fg_color, bg=bg_color).grid(row=0, column=0, padx=5, pady=5)
entrada_ip = tk.Entry(frame_conexion, bg=entry_bg, fg=fg_color, font=("Arial", 12))
entrada_ip.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_conexion, text="Puerto:", fg=fg_color, bg=bg_color).grid(row=1, column=0, padx=5, pady=5)
entrada_puerto = tk.Entry(frame_conexion, bg=entry_bg, fg=fg_color, font=("Arial", 12))
entrada_puerto.grid(row=1, column=1, padx=5, pady=5)

boton_conectar = tk.Button(frame_conexion, text="Conectar", command=conectar_servidor, bg=btn_bg, fg=btn_fg, font=("Arial", 12))
boton_conectar.grid(row=2, columnspan=2, pady=10)

texto = ScrolledText(root, state=tk.DISABLED, width=50, height=20, bg=entry_bg, fg=fg_color, font=("Arial", 12))
texto.pack(padx=10, pady=10)

entrada_mensaje = tk.Entry(root, width=40, bg=entry_bg, fg=fg_color, font=("Arial", 12))
entrada_mensaje.pack(side=tk.LEFT, padx=5)

boton_enviar = tk.Button(root, text="Enviar", command=enviar_mensaje, bg=btn_bg, fg=btn_fg, font=("Arial", 12))
boton_enviar.pack(side=tk.LEFT, padx=5, pady=10)

# Botones adicionales
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
for boton in [boton_conectar, boton_enviar, boton_limpiar, boton_menu]:
    boton.bind("<Enter>", lambda event, boton=boton: on_enter(event, boton))
    boton.bind("<Leave>", lambda event, boton=boton: on_leave(event, boton))

root.mainloop()
