import paramiko
import tkinter as tk
from tkinter import messagebox

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

def ejecutar_comando_bloquear():
    host = host_entry.get()
    usuario = usuario_entry.get()
    contraseña = contraseña_entry.get()
    comando_bloquear_teclado = f"echo '{contraseña}' | sudo -S killall -STOP gnome-shell"

    salida_bloquear_teclado, error_bloquear_teclado = ejecutar_comando_ssh(host, usuario, contraseña, comando_bloquear_teclado)
    if error_bloquear_teclado:
        messagebox.showerror("Error", error_bloquear_teclado)
    else:
        messagebox.showinfo("Éxito", "Bloqueo de teclado y ratón exitoso.")

def ejecutar_comando_desbloquear():
    host = host_entry.get()
    usuario = usuario_entry.get()
    contraseña = contraseña_entry.get()
    comando_desbloquear_teclado = f"echo '{contraseña}' | sudo -S killall -CONT gnome-shell"

    salida_desbloquear_teclado, error_desbloquear_teclado = ejecutar_comando_ssh(host, usuario, contraseña, comando_desbloquear_teclado)
    if error_desbloquear_teclado:
        messagebox.showerror("Error", error_desbloquear_teclado)
    else:
        messagebox.showinfo("Éxito", "Desbloqueo de teclado y ratón exitoso.")

def habilitar_botones(event=None):
    if host_entry.get() and usuario_entry.get() and contraseña_entry.get():
        btn_bloquear.config(state=tk.NORMAL)
        btn_desbloquear.config(state=tk.NORMAL)
    else:
        btn_bloquear.config(state=tk.DISABLED)
        btn_desbloquear.config(state=tk.DISABLED)

def regresar_menu_principal():
    if messagebox.askyesno("Confirmación", "¿Seguro que deseas regresar al menú principal?"):
        root.destroy()

# Configuración de la ventana principal
root = tk.Tk()
root.title("Control Remoto")
root.geometry("420x500")
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
header = tk.Label(root, text="Control de Teclado y Mouse", font=("Helvetica", 16, "bold"), bg=bg_color, fg=fg_color)
header.pack(pady=15)

# Formulario
form_frame = tk.Frame(root, bg=bg_color)
form_frame.pack(pady=20, fill="x", padx=30)

tk.Label(form_frame, text="IP de la computadora:", bg=bg_color, fg=fg_color, anchor="w").pack(fill="x", pady=5)
host_entry = tk.Entry(form_frame, bg=entry_bg, fg=fg_color, relief="groove", highlightthickness=1)
host_entry.pack(fill="x", pady=5)
host_entry.bind("<KeyRelease>", habilitar_botones)

tk.Label(form_frame, text="Usuario:", bg=bg_color, fg=fg_color, anchor="w").pack(fill="x", pady=5)
usuario_entry = tk.Entry(form_frame, bg=entry_bg, fg=fg_color, relief="groove", highlightthickness=1)
usuario_entry.pack(fill="x", pady=5)
usuario_entry.bind("<KeyRelease>", habilitar_botones)

tk.Label(form_frame, text="Contraseña:", bg=bg_color, fg=fg_color, anchor="w").pack(fill="x", pady=5)
contraseña_entry = tk.Entry(form_frame, show="*", bg=entry_bg, fg=fg_color, relief="groove", highlightthickness=1)
contraseña_entry.pack(fill="x", pady=5)
contraseña_entry.bind("<KeyRelease>", habilitar_botones)

# Botones
btn_frame = tk.Frame(root, bg=bg_color)
btn_frame.pack(pady=15)

btn_bloquear = tk.Button(btn_frame, text="Bloquear", command=ejecutar_comando_bloquear, state=tk.DISABLED, bg=btn_bg, fg=btn_fg, activebackground=btn_hover, activeforeground=btn_fg, relief="ridge")
btn_bloquear.grid(row=0, column=0, padx=10)

btn_desbloquear = tk.Button(btn_frame, text="Desbloquear", command=ejecutar_comando_desbloquear, state=tk.DISABLED, bg=btn_bg, fg=btn_fg, activebackground=btn_hover, activeforeground=btn_fg, relief="ridge")
btn_desbloquear.grid(row=0, column=1, padx=10)

btn_cancelar = tk.Button(root, text="Regresar al Menú", command=regresar_menu_principal, bg=btn_hover, fg=btn_fg, activebackground=btn_bg, activeforeground=btn_fg, relief="ridge")
btn_cancelar.pack(pady=20)

# Mensaje de pie de página
footer = tk.Label(root, text="Desarrollado con Tkinter y Paramiko", font=("Helvetica", 10), bg=bg_color, fg=fg_color)
footer.pack(side="bottom", pady=10)

# Iniciar la aplicación
root.mainloop()
