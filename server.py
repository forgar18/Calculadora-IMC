#!/usr/bin/env python3
import socket
import threading
import json

# Dirección IP y puerto donde escuchará el servidor
HOST = "0.0.0.0"   # Escucha en todas las interfaces de red disponibles
PORT = 5000        # Puerto TCP del servidor

# -------------------------------------------------------
# FUNCIONES LÓGICAS DE CÁLCULO DEL IMC
# -------------------------------------------------------

def calcular_imc(peso_kg: float, altura_m: float) -> float:
    """
    Calcula el Índice de Masa Corporal (IMC).
    
    Fórmula: IMC = peso (kg) / (altura (m))²
    """
    return peso_kg / (altura_m ** 2)


def categoria_imc(imc: float) -> str:
    """
    Clasifica el IMC en una categoría de acuerdo con los valores estándar:
    - Menor de 18.5 → Bajo peso
    - 18.5 a 24.9 → Normal
    - 25.0 a 29.9 → Sobrepeso
    - 30.0 o más → Obesidad
    """
    if imc < 18.5:
        return "Bajo peso"
    elif imc < 25.0:
        return "Normal"
    elif imc < 30.0:
        return "Sobrepeso"
    else:
        return "Obesidad"

# -------------------------------------------------------
# PROCESAMIENTO Y VALIDACIÓN DE DATOS RECIBIDOS DEL CLIENTE
# -------------------------------------------------------

def construir_respuesta(data):
    """
    Procesa los datos recibidos del cliente, valida que sean correctos,
    calcula el IMC y devuelve una respuesta en formato JSON con:
      - IMC calculado
      - Categoría del IMC
      - Mensaje descriptivo
      - Sexo y edad (si fueron enviados)

    Si hay errores de formato o datos inválidos, devuelve un mensaje de error.
    """
    try:
        # Extrae los datos del diccionario recibido
        sexo = str(data.get("sexo", "")).strip()
        edad = int(data.get("edad", 0))
        altura = float(data.get("altura", 0.0))
        peso = float(data.get("peso", 0.0))

        # Validación básica de datos
        if altura <= 0 or peso <= 0 or edad <= 0:
            return {"error": "Datos inválidos: altura, peso y edad deben ser > 0."}

        # Cálculo del IMC y categoría
        imc_val = calcular_imc(peso, altura)
        cat = categoria_imc(imc_val)

        # Construcción del mensaje descriptivo
        respuesta_texto = (
            f"IMC = {imc_val:.2f}. Categoría: {cat}. "
            "Tabla: <18.5 Bajo peso | 18.5-24.9 Normal | 25-29.9 Sobrepeso | >=30 Obesidad."
        )

        # Devuelve un diccionario (que luego se convierte a JSON)
        return {
            "imc": round(imc_val, 2),
            "categoria": cat,
            "mensaje": respuesta_texto,
            "sexo": sexo,
            "edad": edad
        }

    except Exception as e:
        # Si ocurre un error en el proceso, devuelve un mensaje de error
        return {"error": f"Error al procesar datos: {str(e)}"}

# -------------------------------------------------------
# MANEJO DE CLIENTES (HILO POR CONEXIÓN)
# -------------------------------------------------------

def handle_client(conn, addr):
    """
    Atiende a un cliente conectado en un hilo independiente.
    - Recibe datos en formato JSON.
    - Procesa los datos (peso, altura, etc.).
    - Devuelve el resultado en formato JSON.
    """
    print(f"[+] Conexión entrante desde {addr}")
    with conn:  # Maneja la conexión de forma segura (se cierra al salir)
        try:
            # Recibe datos del cliente (máx. 4096 bytes)
            raw = conn.recv(4096)
            if not raw:
                print("[-] Cliente cerró sin enviar datos")
                return

            # Intenta decodificar los datos como JSON
            try:
                payload = json.loads(raw.decode('utf-8'))
            except json.JSONDecodeError:
                # Si el formato no es válido, envía un error al cliente
                response = {"error": "Formato JSON inválido."}
                conn.sendall(json.dumps(response).encode('utf-8'))
                return

            # Procesa los datos válidos y construye la respuesta
            result = construir_respuesta(payload)

            # Envía la respuesta al cliente
            conn.sendall(json.dumps(result).encode('utf-8'))

        except Exception as e:
            # Muestra en consola si hay un error con ese cliente
            print(f"[!] Error manejando cliente {addr}: {e}")

# -------------------------------------------------------
# CONFIGURACIÓN Y EJECUCIÓN DEL SERVIDOR TCP
# -------------------------------------------------------

def start_server(host=HOST, port=PORT):
    """
    Inicia el servidor TCP multicliente.
    - Escucha conexiones en la IP y puerto especificados.
    - Crea un hilo para cada cliente conectado.
    """
    print(f"[i] Iniciando servidor IMC en {host}:{port}")

    # Crea el socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))   # Asigna IP y puerto
        s.listen()             # Pone el servidor en modo escucha
        print("[i] Servidor escuchando. Esperando clientes...")

        # Bucle infinito: atiende conexiones una a una
        while True:
            conn, addr = s.accept()  # Espera una conexión entrante
            # Crea un hilo para atender al cliente sin bloquear al servidor
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()

# -------------------------------------------------------
# PUNTO DE ENTRADA PRINCIPAL
# -------------------------------------------------------

if __name__ == "__main__":
    # Solo se ejecuta si este archivo se corre directamente
    start_server()
