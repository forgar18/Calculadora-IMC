Repositorio: (https://github.com/forgar18/Calculadora-IMC)

# 🧠 Proyecto IMC Remoto - Cliente/Servidor con TCP

## 📘 Descripción
Este proyecto implementa una aplicación **Cliente-Servidor** en **Python** utilizando **sockets TCP** para calcular el **Índice de Masa Corporal (IMC)** de manera remota.  

El servidor recibe desde el cliente los datos del usuario (sexo, edad, altura y peso), calcula el IMC, determina la categoría correspondiente y devuelve los resultados al cliente a través de la red.

---

## 🎯 Objetivo General
Reforzar los conocimientos del protocolo **TCP/IP** mediante la implementación de un programa distribuido que procese solicitudes y respuestas entre cliente y servidor.

---

## ⚙️ Funcionamiento

### 🖥️ Servidor (`server.py`)
- Escucha permanentemente conexiones de clientes en la red.
- Recibe datos del cliente en formato **JSON**.
- Calcula el **IMC** usando la fórmula:
  \[
  IMC = \frac{peso (kg)}{altura (m)^2}
  \]
- Determina la categoría del IMC:
  - **< 18.5:** Bajo peso  
  - **18.5 – 24.9:** Normal  
  - **25.0 – 29.9:** Sobrepeso  
  - **≥ 30.0:** Obesidad
- Envía la respuesta al cliente con el IMC calculado y su respectiva categoría.

### 💻 Cliente (`cliente.py`)
- Solicita al usuario los datos: sexo, edad, altura (m) y peso (kg).
- Envía los datos al servidor mediante una conexión TCP.
- Recibe la respuesta del servidor y muestra en pantalla el resultado del IMC.

---

## 🧩 Requisitos
- Python 3.8 o superior
- Conexión entre ambos equipos en la **misma red local**
- (Opcional) Wireshark para capturar el tráfico TCP entre cliente y servidor

---

## 🛠️ Ejecución

### En el **servidor (Ubuntu)**
1. Abre una terminal en la carpeta del proyecto.
2. Ejecuta el servidor:
   ```bash
   python3 server.py

### En el **cliente (windows)**
3. Abre una terminal en la carpeta del proyecto.
4. Ejecuta el servidor:
   ```bash
   python3 cliente.py

📡 Monitoreo con Wireshark

Para analizar la comunicación entre cliente y servidor:

Abre Wireshark.

Selecciona la interfaz de red VirtualBox Host-Only Network.

Aplica el filtro:

tcp.port == 5000


Ejecuta el cliente y observa el intercambio de paquetes TCP entre ambos sistemas.

🧠 Ejemplo de ejecución

Cliente:

Sexo (M/F/O): M
Edad (años): 22
Altura en metros (ej. 1.75): 1.80
Peso en kg (ej. 68.5): 70
[i] Conectando a 192.168.1.11:5000 ...
--- Resultado IMC ---
IMC: 21.60
Categoría: Peso normal
Tienes un peso saludable. ¡Sigue así!
---------------------
