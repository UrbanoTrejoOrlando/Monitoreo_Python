# Monitoreo_Python

Repositorio para scripts de monitoreo desarrollados en **Python**.

---

## Tabla de contenido

1. [Descripción](#descripción)  
2. [Características principales](#características-principales)  
3. [Estructura del proyecto](#estructura-del-proyecto)  
4. [Requisitos](#requisitos)  
5. [Instalación](#instalación)  
6. [Uso](#uso)  

---

## Descripción

Este proyecto contiene uno o más scripts en Python orientados al monitoreo de recursos, servicios o datos. Puede utilizarse para supervisar disponibilidad, rendimiento, registrar métricas a lo largo del tiempo o generar alertas.

---

## Características principales

- Monitoreo de servicios o endpoints  
- Registro de métricas periódicas  
- Envío de alertas (por ejemplo, por correo, logs, o integración externa)  
- Posible generación de reportes o dashboards  
- Automatización de tareas de monitoreo  

---

## Estructura del proyecto

## Descripción de los scripts

| Archivo | Descripción |
|----------|-------------|
| **menu.py** | Menú principal para ejecutar las distintas funciones del sistema. |
| **monitoreo.py** | Script encargado de recopilar información o controlar dispositivos conectados. |
| **chatServidor.py** y **chatCliente.py** | Implementan un sistema de chat en tiempo real entre servidor y cliente. |
| **enviar_servidor.py** y **enviar_cliente.py** | Scripts para enviar archivos o mensajes entre dispositivos. |
| **pantallas_servidor.py** y **pantallas_clientes.py** | Scripts para monitorear o controlar pantallas de los equipos conectados. |
| **bloquearTeclado.py** | Bloquea temporalmente el uso del teclado en el sistema. |
| **bloquearpagina.py** | Bloquea el acceso a determinadas páginas web. |
| **denegarping.py** | Desactiva las respuestas a solicitudes de ping (ICMP) para mejorar la seguridad. |
| **apagar.py** | Permite apagar el sistema remoto o local mediante comando Python. |

---

## Requisitos

- **Python 3.8+**
- Librerías estándar (no requiere dependencias externas en la mayoría de los casos)
- Ejecución en sistemas **Linux (Fedora, Arch, Ubuntu, etc.)** o compatibles
- Permisos de administrador (para scripts que afectan red, teclado o apagado)

---

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/UrbanoTrejoOrlando/Monitoreo_Python.git
   
2. Entra en el directorio:
   ```bash
    cd Monitoreo_Python

3. (Opcional) Crea un entorno virtual:
   ```bash
    python3 -m venv venv
    source venv/bin/activate

## Uso
Ejecuta el menú principal para seleccionar la función deseada:
   ```bash
  python3 menu.py

