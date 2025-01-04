import socket
import tkinter as tk
from tkinter import filedialog, messagebox

# Función para seleccionar un archivo
def select_file():
    file_path = filedialog.askopenfilename()
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(0, file_path)

# Función para enviar el archivo
def send_file():
    file_path = entry_file_path.get()
    server_ip = entry_server_ip.get()

    if not file_path or not server_ip:
        messagebox.showerror("Error", "Por favor ingresa todos los campos.")
        return

    try:
        # Conexión al servidor
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, 65432))

        # Enviar el nombre del archivo
        filename = file_path.split('/')[-1]
        client_socket.send(filename.encode())

        # Enviar el archivo
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                client_socket.send(chunk)

        client_socket.close()
        messagebox.showinfo("Éxito", f"Archivo {filename} enviado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Función para regresar al menú principal
def regresar_menu_principal():
    if messagebox.askyesno("Confirmación", "¿Seguro que deseas regresar al menú principal?"):
        root.destroy()

# Configuración de la ventana principal
root = tk.Tk()
root.title("Envío de Archivos")
root.geometry("500x300")
root.resizable(False, False)

# Tema de colores en tonos azules
bg_color = "#d8eefe"  # Fondo general azul claro
fg_color = "#002f6c"  # Texto azul oscuro
entry_bg = "#ffffff"  # Fondo de entrada blanco
btn_bg = "#007bff"    # Botones azul vibrante
btn_hover = "#0056b3" # Botones al pasar el mouse en azul más oscuro
btn_fg = "#ffffff"    # Texto de los botones en blanco

root.configure(bg=bg_color)

# Encabezado
header = tk.Label(root, text="Envío de Archivos", font=("Helvetica", 16, "bold"), bg=bg_color, fg=fg_color)
header.pack(pady=15)

# Formulario
form_frame = tk.Frame(root, bg=bg_color)
form_frame.pack(pady=10, fill="x", padx=30)

tk.Label(form_frame, text="IP del Servidor:", bg=bg_color, fg=fg_color, anchor="w").grid(row=0, column=0, sticky="w", pady=5)
entry_server_ip = tk.Entry(form_frame, bg=entry_bg, fg=fg_color, relief="groove", highlightthickness=1)
entry_server_ip.grid(row=0, column=1, pady=5, padx=10)

tk.Label(form_frame, text="Ruta del Archivo:", bg=bg_color, fg=fg_color, anchor="w").grid(row=1, column=0, sticky="w", pady=5)
entry_file_path = tk.Entry(form_frame, bg=entry_bg, fg=fg_color, relief="groove", highlightthickness=1)
entry_file_path.grid(row=1, column=1, pady=5, padx=10)

btn_browse = tk.Button(form_frame, text="Seleccionar Archivo", command=select_file, bg=btn_bg, fg=btn_fg, activebackground=btn_hover, activeforeground=btn_fg, relief="ridge")
btn_browse.grid(row=1, column=2, pady=5, padx=10)

# Botones
btn_frame = tk.Frame(root, bg=bg_color)
btn_frame.pack(pady=20)

btn_send = tk.Button(btn_frame, text="Enviar Archivo", command=send_file, bg=btn_bg, fg=btn_fg, activebackground=btn_hover, activeforeground=btn_fg, relief="ridge")
btn_send.grid(row=0, column=0, padx=10)

btn_cancelar = tk.Button(btn_frame, text="Regresar al Menú", command=regresar_menu_principal, bg=btn_hover, fg=btn_fg, activebackground=btn_bg, activeforeground=btn_fg, relief="ridge")
btn_cancelar.grid(row=0, column=1, padx=10)

# Mensaje de pie de página
footer = tk.Label(root, text="Desarrollado con Tkinter y Sockets", font=("Helvetica", 10), bg=bg_color, fg=fg_color)
footer.pack(side="bottom", pady=10)

# Iniciar la aplicación
root.mainloop()
