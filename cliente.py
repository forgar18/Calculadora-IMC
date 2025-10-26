#!/usr/bin/env python3
"""
client.py - Cliente TCP para calcular IMC remoto
Descripción:
Este cliente se conecta mediante sockets TCP a un servidor remoto
que calcula el IMC (Índice de Masa Corporal). El cliente solicita
al usuario sus datos personales (sexo, edad, altura y peso),
envía esta información al servidor en formato JSON, recibe la
respuesta con el resultado del IMC y la muestra en pantalla.
"""

import socket   # Librería estándar de Python para manejar conexiones de red
import json     # Para codificar y decodificar mensajes en formato JSON

# Dirección IP y puerto del servidor (debe estar en la misma red)
SERVER_IP = "192.168.1.11"
SERVER_PORT = 5000


def pedir_datos_usuario():
    """
    Solicita al usuario los datos necesarios para el cálculo del IMC.

    Retorna:
        dict: diccionario con las claves 'sexo', 'edad', 'altura' y 'peso'
    """
    sexo = input("Sexo (M/F/O): ").strip()                # M: masculino, F: femenino, O: otro
    edad = input("Edad (años): ").strip()
    altura = input("Altura en metros (ej. 1.75): ").strip()
    peso = input("Peso en kg (ej. 68.5): ").strip()

    return {
        "sexo": sexo,
        "edad": edad,
        "altura": altura,
        "peso": peso
    }


def main():
    """
    Función principal del cliente:
    - Pide los datos al usuario.
    - Crea una conexión TCP al servidor.
    - Envía los datos codificados en JSON.
    - Espera la respuesta del servidor con el resultado del IMC.
    - Muestra el resultado al usuario.
    """
    # Obtener datos desde teclado
    datos = pedir_datos_usuario()

    # Convertir el diccionario a texto JSON y luego a bytes para enviar por red
    payload = json.dumps(datos).encode('utf-8')

    try:
        # Crear socket TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"[i] Conectando a {SERVER_IP}:{SERVER_PORT} ...")

            # Conexión con el servidor
            s.connect((SERVER_IP, SERVER_PORT))

            # Envío de los datos codificados
            s.sendall(payload)

            # Esperar respuesta del servidor (hasta 4 KB)
            respuesta_raw = s.recv(4096)
            if not respuesta_raw:
                print("[-] No se recibió respuesta del servidor.")
                return

            # Decodificar la respuesta de bytes a JSON
            respuesta = json.loads(respuesta_raw.decode('utf-8'))

            # Mostrar resultados o errores
            if "error" in respuesta:
                print(f"Error del servidor: {respuesta['error']}")
            else:
                print("\n--- Resultado IMC ---")
                print(f"IMC: {respuesta.get('imc')}")
                print(f"Categoría: {respuesta.get('categoria')}")
                print(respuesta.get('mensaje'))
                print("---------------------\n")

    except ConnectionRefusedError:
        # Error cuando el servidor no está disponible o IP/puerto son incorrectos
        print("[-] No se pudo conectar al servidor. Verifica IP/puerto y que el servidor esté corriendo.")

    except Exception as e:
        # Cualquier otro error inesperado
        print(f"[!] Error de cliente: {e}")


# Punto de entrada del programa
if __name__ == "__main__":
    main()
