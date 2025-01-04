import tkinter as tk
from tkinter import messagebox
import subprocess
import re

# Colores
bg_color = "#d8eefe"  # Fondo general azul claro
fg_color = "#002f6c"  # Texto azul oscuro
entry_bg = "#ffffff"  # Fondo de entrada blanco
btn_bg = "#007bff"    # Botones azul vibrante
btn_hover = "#0056b3" # Botones al pasar el mouse en azul más oscuro
btn_fg = "#ffffff"    # Texto de los botones en blanco

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando el comando: {e.stderr.decode()}")

def check_rule_exists(command):
    try:
        subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def allow_ping(ip):
    check_command = f"sudo iptables -C INPUT -p icmp --icmp-type echo-request -s {ip} -j DROP"
    if check_rule_exists(check_command):
        command = f"sudo iptables -D INPUT -p icmp --icmp-type echo-request -s {ip} -j DROP"
        run_command(command)
    
    command = f"sudo iptables -I INPUT -p icmp --icmp-type echo-request -s {ip} -j ACCEPT"
    run_command(command)
    print(f"Ping permitido desde la IP {ip}")

def deny_ping(ip):
    check_command = f"sudo iptables -C INPUT -p icmp --icmp-type echo-request -s {ip} -j ACCEPT"
    if check_rule_exists(check_command):
        command = f"sudo iptables -D INPUT -p icmp --icmp-type echo-request -s {ip} -j ACCEPT"
        run_command(command)
    
    command = f"sudo iptables -I INPUT -p icmp --icmp-type echo-request -s {ip} -j DROP"
    run_command(command)
    print(f"Ping denegado desde la IP {ip}")

def validate_ip(ip):
    ip_regex = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    if ip_regex.match(ip):
        segments = ip.split(".")
        if all(0 <= int(segment) <= 255 for segment in segments):
            return True
    return False

def execute_action(action, ip):
    if not ip:
        messagebox.showerror("Error", "Por favor, ingresa una dirección IP.")
        return
    if not validate_ip(ip):
        messagebox.showerror("Error", "La dirección IP ingresada no es válida.")
        return
    
    if action == 'permitir':
        allow_ping(ip)
        messagebox.showinfo("Acción completada", f"Ping permitido desde la IP {ip}.")
    elif action == 'denegar':
        deny_ping(ip)
        messagebox.showinfo("Acción completada", f"Ping denegado desde la IP {ip}.")
    else:
        messagebox.showerror("Error", "Acción no válida.")

def main_menu():
    root = tk.Tk()
    root.title("Gestión de Pings")
    root.geometry("400x300")
    root.configure(bg=bg_color)

    title_label = tk.Label(root, text="Gestión de Pings", font=("Arial", 16, "bold"), bg=bg_color, fg=fg_color)
    title_label.pack(pady=20)

    action_button = tk.Button(root, text="Configurar Reglas de Ping", command=lambda: [root.destroy(), open_configuration_window()],
                              bg=btn_bg, fg=btn_fg, font=("Arial", 12), activebackground=btn_hover)
    action_button.pack(pady=10)

    exit_button = tk.Button(root, text="Salir", command=root.quit, bg=btn_bg, fg=btn_fg, font=("Arial", 12), activebackground=btn_hover)
    exit_button.pack(pady=10)

    root.mainloop()

def open_configuration_window():
    config_window = tk.Tk()
    config_window.title("Configurar Pings")
    config_window.geometry("400x300")
    config_window.configure(bg=bg_color)

    action_label = tk.Label(config_window, text="Selecciona una acción:", font=("Arial", 12), bg=bg_color, fg=fg_color)
    action_label.pack(pady=10)

    action_variable = tk.StringVar(config_window)
    action_variable.set("Seleccione la acción")

    action_menu = tk.OptionMenu(config_window, action_variable, "permitir", "denegar")
    action_menu.config(bg=btn_bg, fg=btn_fg, activebackground=btn_hover, font=("Arial", 10))
    action_menu["menu"].config(bg=btn_bg, fg=btn_fg)
    action_menu.pack(pady=10)

    ip_label = tk.Label(config_window, text="Ingresa la dirección IP:", font=("Arial", 12), bg=bg_color, fg=fg_color)
    ip_label.pack(pady=10)

    ip_entry = tk.Entry(config_window, width=30, font=("Arial", 12), bg=entry_bg)
    ip_entry.pack(pady=10)

    execute_button = tk.Button(config_window, text="Ejecutar", command=lambda: execute_action(action_variable.get(), ip_entry.get()),
                                bg=btn_bg, fg=btn_fg, font=("Arial", 12), activebackground=btn_hover)
    execute_button.pack(pady=10)

    back_button = tk.Button(config_window, text="Menú Principal", command=lambda: [config_window.destroy(), main_menu()],
                             bg=btn_bg, fg=btn_fg, font=("Arial", 12), activebackground=btn_hover)
    back_button.pack(pady=10)

    config_window.mainloop()

# Iniciar la aplicación
main_menu()
