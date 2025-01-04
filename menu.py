import tkinter as tk
from tkinter import messagebox
import os

# Crear la ventana principal
root = tk.Tk()
root.title("Menú de Monitoreo")
root.geometry("480x600")
root.configure(bg="#f4f4f4")  # Fondo claro minimalista

# Función para actualizar la barra de estado
def actualizar_estado(mensaje):
    barra_estado.config(text=mensaje)

# Función para mostrar mensajes de confirmación
def mostrar_confirmacion(mensaje):
    messagebox.showinfo("Confirmación", mensaje)

# Crear un título
titulo = tk.Label(root, text="Menú de Monitoreo", font=("Helvetica", 18, "bold"), bg="#f4f4f4", fg="#333333")
titulo.pack(pady=10)

# Crear un marco para los botones
frame_botones = tk.Frame(root, bg="#f4f4f4")
frame_botones.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)

# Definir estilo minimalista para botones
button_style = {
    "font": ("Helvetica", 10, "normal"),
    "bd": 0,
    "relief": tk.FLAT,
    "height": 2,
    "width": 20,
    "highlightthickness": 1,
    "highlightbackground": "#cccccc",  # Sutil borde gris claro
}

# Funciones de ejecución de scripts (ya están definidas)
def monitoreo_cliente():
    os.system("python3 /home/starlord/Documents/Proyecto_Anselmo/pantallas_clientes.py")
    mostrar_confirmacion("Monitoreo en cliente ejecutado")
    actualizar_estado("Monitoreo en cliente ejecutado")

def monitoreo_servidor():
    os.system("python3 /home/starlord/Documents/Proyecto_Anselmo/pantallas_servidor.py")
    mostrar_confirmacion("Monitoreo en servidor ejecutado")
    actualizar_estado("Monitoreo en servidor ejecutado")

def envioArchivos_cliente():
    os.system("python3 /home/starlord/Documents/Proyecto_Anselmo/enviar_cliente.py")
    mostrar_confirmacion("Envío de archivos en cliente ejecutado")
    actualizar_estado("Envío de archivos en cliente ejecutado")

def envioArchivos_servidor():
    os.system("python3 /home/starlord/Documents/Proyecto_Anselmo/enviar_servidor.py")
    mostrar_confirmacion("Envío de archivos en servidor ejecutado")
    actualizar_estado("Envío de archivos en servidor ejecutado")

def ejecutar_bloqueo_teclado_mouse():
    os.system("python3 /home/starlord/Documents/Proyecto_Anselmo/bloquearTM.py")
    mostrar_confirmacion("Bloqueo de teclado y mouse ejecutado")
    actualizar_estado("Bloqueo de teclado y mouse ejecutado")

def ejecutar_apagar_pc():
    os.system("python3 /home/starlord/Documents/Proyecto_Anselmo/apagar.py")
    mostrar_confirmacion("Apagar PC remoto ejecutado")
    actualizar_estado("Apagar PC remoto ejecutado")

def denegar_permitir_ping():
    os.system("python3 /home/starlord/Documents/Proyecto_Anselmo/denegarping.py")
    mostrar_confirmacion("Denegar ping remoto ejecutado")
    actualizar_estado("Denegar ping remoto ejecutado")

def chat_cliente():
    os.system("python3 /home/starlord/Documents/Proyecto_Anselmo/chatCliente.py")
    mostrar_confirmacion("Chat cliente ejecutado")
    actualizar_estado("Chat cliente ejecutado")

def chat_servidor():
    os.system("python3 /home/starlord/Documents/Proyecto_Anselmo/chatServidor.py")
    mostrar_confirmacion("Chat servidor ejecutado")
    actualizar_estado("Chat servidor ejecutado")

def ejecutar_bloqueo_paginas():
    os.system("python3 /home/starlord/Documents/Proyecto_Anselmo/bloquearpaginaa.py")
    mostrar_confirmacion("Bloqueo de páginas ejecutado")
    actualizar_estado("Bloqueo de páginas ejecutado")

# Lista de botones con etiquetas y funciones
botones = [
    ("Monitoreo en cliente", monitoreo_cliente),
    ("Monitoreo en servidor", monitoreo_servidor),
    ("Envio de Archivos en cliente", envioArchivos_cliente),
    ("Envio de Archivos en servidor", envioArchivos_servidor),
    ("Bloqueo de teclado y mouse", ejecutar_bloqueo_teclado_mouse),
    ("Apagar el PC remoto", ejecutar_apagar_pc),
    ("Denegar y permitir ping remoto", denegar_permitir_ping),
    ("Chat cliente", chat_cliente),
    ("Chat servidor", chat_servidor),
]

# Colocar los primeros botones en una cuadrícula de dos columnas
for idx, (texto, comando) in enumerate(botones):
    row = idx // 2
    col = idx % 2
    boton = tk.Button(
        frame_botones, text=texto, command=comando, bg="#ffffff", fg="#333333", **button_style
    )
    boton.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

# Configurar el grid del frame para expandirse
for i in range(2):
    frame_botones.grid_columnconfigure(i, weight=1)

# Colocar el botón de bloqueo de páginas en el centro
boton_bloqueo_paginas = tk.Button(
    root, text="Bloqueo de páginas", command=ejecutar_bloqueo_paginas, bg="#ffffff", fg="#333333", **button_style
)
boton_bloqueo_paginas.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

# Crear botón para salir
boton_salir = tk.Button(
    root, text="Salir", command=root.quit, bg="#e74c3c", fg="#f4f4f4", **button_style
)
boton_salir.pack(pady=20)

# Crear una barra de estado estilizada
barra_estado = tk.Label(root, text="Listo", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#333333", fg="#f4f4f4", font=("Helvetica", 9))
barra_estado.pack(side=tk.BOTTOM, fill=tk.X)

# Ejecutar la ventana principal
root.mainloop()

