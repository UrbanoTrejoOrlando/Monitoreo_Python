import paramiko
import tkinter as tk
from tkinter import messagebox

# Colores personalizados
bg_color = "#d8eefe"  # Fondo general azul claro
fg_color = "#002f6c"  # Texto azul oscuro
entry_bg = "#ffffff"  # Fondo de entrada blanco
btn_bg_block = "#ff4d4d"  # Botón de bloqueo rojo
btn_bg_unblock = "#007bff"  # Botón de desbloqueo azul
btn_hover = "#0056b3"  # Hover para botones
btn_fg = "#ffffff"  # Texto de los botones en blanco

def execute_remote_command(host, username, password, command):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password)
        transport = ssh.get_transport()
        session = transport.open_session()
        session.set_combine_stderr(True)
        session.get_pty()
        session.exec_command(command)
        
        stdin = session.makefile('wb', -1)
        stdout = session.makefile('rb', -1)
        stderr = session.makefile_stderr('rb', -1)

        stdin.write(f'{password}\n')
        stdin.flush()

        output = stdout.read().decode()
        error = stderr.read().decode()

        ssh.close()
        return output, error
    except Exception as e:
        return None, str(e)

def block_websites_remote():
    host = entry_host.get()
    username = entry_user.get()
    password = entry_password.get()
    domains = entry_domains.get().split(',')

    commands = ["echo '0.0.0.0 {}' | sudo tee -a /etc/hosts".format(domain.strip()) for domain in domains]
    commands += ["echo '0.0.0.0 www.{}' | sudo tee -a /etc/hosts".format(domain.strip()) for domain in domains]
    commands.append("sudo systemctl restart network-manager")
    command = " && ".join(commands)
    
    output, error = execute_remote_command(host, username, password, command)
    if error:
        messagebox.showerror("Error", f"Error al bloquear sitios web: {error}")
    else:
        messagebox.showinfo("Éxito", f"Acceso denegado para los dominios: {', '.join(domains)}")

def unblock_websites_remote():
    host = entry_host.get()
    username = entry_user.get()
    password = entry_password.get()
    domains = entry_domains.get().split(',')

    commands = ["sudo sed -i '/{}$/d' /etc/hosts".format(domain.strip()) for domain in domains]
    commands += ["sudo sed -i '/www.{}$/d' /etc/hosts".format(domain.strip()) for domain in domains]
    commands.append("sudo systemctl restart network-manager")
    command = " && ".join(commands)
    
    output, error = execute_remote_command(host, username, password, command)
    if error:
        messagebox.showerror("Error", f"Error al restaurar acceso para los sitios web: {error}")
    else:
        messagebox.showinfo("Éxito", f"Acceso restaurado para los dominios: {', '.join(domains)}")

def habilitar_botones(event=None):
    if entry_host.get() and entry_user.get() and entry_password.get() and entry_domains.get():
        btn_block.config(state=tk.NORMAL)
        btn_unblock.config(state=tk.NORMAL)
    else:
        btn_block.config(state=tk.DISABLED)
        btn_unblock.config(state=tk.DISABLED)

def regresar_menu():
    root.destroy()  # Aquí puedes añadir la lógica para regresar al menú principal si lo deseas.

# Crear la ventana principal
root = tk.Tk()
root.title("Bloqueo de Páginas Web")
root.geometry("600x350")
root.resizable(False, False)
root.configure(bg=bg_color)

# Obtener dimensiones de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calcular la posición para centrar la ventana
x = (screen_width // 2) - (600 // 2)
y = (screen_height // 2) - (350 // 2)

root.geometry(f"700x350+{x}+{y}")

# Crear y organizar los widgets
tk.Label(root, text="IP de la Computadora:", bg=bg_color, fg=fg_color).grid(row=0, column=0, padx=10, pady=5)
entry_host = tk.Entry(root, width=50, bg=entry_bg, fg=fg_color)
entry_host.grid(row=0, column=1, padx=10, pady=5)
entry_host.bind("<KeyRelease>", habilitar_botones)

tk.Label(root, text="Nombre de usuario de la computadora:", bg=bg_color, fg=fg_color).grid(row=1, column=0, padx=10, pady=5)
entry_user = tk.Entry(root, width=50, bg=entry_bg, fg=fg_color)
entry_user.grid(row=1, column=1, padx=10, pady=5)
entry_user.bind("<KeyRelease>", habilitar_botones)

tk.Label(root, text="Contraseña de la computadora:", bg=bg_color, fg=fg_color).grid(row=2, column=0, padx=10, pady=5)
entry_password = tk.Entry(root, width=50, show='*', bg=entry_bg, fg=fg_color)
entry_password.grid(row=2, column=1, padx=10, pady=5)
entry_password.bind("<KeyRelease>", habilitar_botones)

tk.Label(root, text="Páginas Web a bloquear:", bg=bg_color, fg=fg_color).grid(row=3, column=0, padx=10, pady=5)
entry_domains = tk.Entry(root, width=50, bg=entry_bg, fg=fg_color)
entry_domains.grid(row=3, column=1, padx=10, pady=5)
entry_domains.bind("<KeyRelease>", habilitar_botones)

btn_block = tk.Button(root, text="Bloquear el acceso", command=block_websites_remote, bg=btn_bg_block, fg=btn_fg, state=tk.DISABLED, font=("Arial", 12))
btn_block.grid(row=4, column=0, padx=10, pady=20)

btn_unblock = tk.Button(root, text="Permitir el Acceso", command=unblock_websites_remote, bg=btn_bg_unblock, fg=btn_fg, state=tk.DISABLED, font=("Arial", 12))
btn_unblock.grid(row=4, column=1, padx=10, pady=20)

# Botón para regresar al menú
btn_regresar = tk.Button(root, text="Regresar al Menú", command=regresar_menu, bg=btn_bg_unblock, fg=btn_fg, font=("Arial", 12))
btn_regresar.grid(row=5, column=0, columnspan=2, pady=10)

# Estilos de hover para botones
def on_enter(event, boton):
    boton['bg'] = btn_hover

def on_leave(event, boton):
    if boton == btn_block:
        boton['bg'] = btn_bg_block
    else:
        boton['bg'] = btn_bg_unblock

# Asociar eventos de hover
for boton in [btn_block, btn_unblock, btn_regresar]:
    boton.bind("<Enter>", lambda event, boton=boton: on_enter(event, boton))
    boton.bind("<Leave>", lambda event, boton=boton: on_leave(event, boton))

# Ejecutar la interfaz
root.mainloop()
