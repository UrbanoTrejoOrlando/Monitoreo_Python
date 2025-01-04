import paramiko
import tkinter as tk
from tkinter import messagebox

# Tema de colores en tonos azules
bg_color = "#d8eefe"  # Fondo general azul claro
fg_color = "#002f6c"  # Texto azul oscuro
entry_bg = "#ffffff"  # Fondo de entrada blanco
btn_bg = "#007bff"    # Botones azul vibrante
btn_hover = "#0056b3" # Botones al pasar el mouse en azul más oscuro
btn_fg = "#ffffff"    # Texto de los botones en blanco

def ejecutar_comando_ssh(host, usuario, contraseña, comando):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=host, username=usuario, password=contraseña)
        stdin, stdout, stderr = ssh_client.exec_command(comando)
        stdin.write(contraseña + '\n')
        stdin.flush()
        salida = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")
        ssh_client.close()
        return salida, error
    except Exception as e:
        return None, str(e)

def ejecutar_apagado():
    host = host_entry.get()
    usuario = usuario_entry.get()
    contraseña = contraseña_entry.get()
    comando_apagado = "sudo -S shutdown -h now"
    comando_contraseña = f"echo '{contraseña}' | {comando_apagado}"

    salida, error = ejecutar_comando_ssh(host, usuario, contraseña, comando_contraseña)

    if error and "contraseña para" in error:
        messagebox.showinfo("Éxito", "El equipo Ubuntu se ha apagado correctamente.")
    else:
        messagebox.showinfo("Éxito", "El equipo Ubuntu se ha apagado correctamente.")

def habilitar_boton(event=None):
    if host_entry.get() and usuario_entry.get() and contraseña_entry.get():
        btn_apagar.config(state=tk.NORMAL)
    else:
        btn_apagar.config(state=tk.DISABLED)

def regresar_menu():
    root.destroy()  # Aquí puedes añadir la lógica para regresar al menú principal si lo deseas.

root = tk.Tk()
root.title("Apagar PC remoto")
root.geometry("380x380")
root.resizable(False, False)
root.configure(bg=bg_color)

# Obtener dimensiones de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calcular la posición para centrar la ventana
x = (screen_width // 2) - (380 // 2)
y = (screen_height // 2) - (380 // 2)

root.geometry(f"380x380+{x}+{y}")

# Título
tk.Label(root, text="Apagar la computadora de un usuario/cliente", bg=bg_color, fg=fg_color, font=("Arial", 14)).pack(pady=10)

# Campos de entrada
tk.Label(root, text="IP de la computadora:", bg=bg_color, fg=fg_color).pack(anchor="w", padx=20)
host_entry = tk.Entry(root, bg=entry_bg, fg=fg_color)
host_entry.pack(fill="x", padx=20)
host_entry.bind("<KeyRelease>", habilitar_boton)

tk.Label(root, text="Nombre de usuario de la computadora:", bg=bg_color, fg=fg_color).pack(anchor="w", padx=20)
usuario_entry = tk.Entry(root, bg=entry_bg, fg=fg_color)
usuario_entry.pack(fill="x", padx=20)
usuario_entry.bind("<KeyRelease>", habilitar_boton)

tk.Label(root, text="Contraseña de la computadora:", bg=bg_color, fg=fg_color).pack(anchor="w", padx=20)
contraseña_entry = tk.Entry(root, show="*", bg=entry_bg, fg=fg_color)
contraseña_entry.pack(fill="x", padx=20)
contraseña_entry.bind("<KeyRelease>", habilitar_boton)

# Botón para apagar
btn_apagar = tk.Button(root, text="Apagar", command=ejecutar_apagado, state=tk.DISABLED, bg=btn_bg, fg=btn_fg, font=("Arial", 12))
btn_apagar.pack(pady=20)

# Botón para regresar al menú
btn_regresar = tk.Button(root, text="Regresar al Menú", command=regresar_menu, bg=btn_bg, fg=btn_fg, font=("Arial", 12))
btn_regresar.pack(pady=10)

# Estilos de hover para botones
def on_enter(event, boton):
    boton['bg'] = btn_hover

def on_leave(event, boton):
    boton['bg'] = btn_bg

# Asociar eventos de hover
for boton in [btn_apagar, btn_regresar]:
    boton.bind("<Enter>", lambda event, boton=boton: on_enter(event, boton))
    boton.bind("<Leave>", lambda event, boton=boton: on_leave(event, boton))

root.mainloop()

