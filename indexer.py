import os
import random
import time

def generar_archivos_prueba():
    os.makedirs(CARPETA_DATOS, exist_ok=True)
    carnet = 20210001

    for i in range(1, TOTAL_ARCHIVOS + 1):
        nombre_archivo = f"estudiantes_{i:03d}.txt"
        ruta = os.path.join(CARPETA_DATOS, nombre_archivo)

        with open(ruta, "w", encoding="utf-8") as f:
            for j in range(REGISTROS_POR_ARCHIVO):
                nombre = random.choice(NOMBRES)
                apellido1 = random.choice(APELLIDOS)
                apellido2 = random.choice(APELLIDOS)
                nombre_completo = f"{apellido1} {apellido2}, {nombre}"
                carrera = random.choice(CARRERAS)
                promedio = round(random.uniform(60.0, 100.0), 1)

                registro = f"{carnet}|{nombre_completo}|{carrera}|{promedio}\n"
                f.write(registro)
                carnet += 1

def generar_indice(carpeta, archivo_indice):
    with open(archivo_indice, "w", encoding="utf-8") as idx:
        for archivo in sorted(os.listdir(carpeta)):
            ruta = os.path.join(carpeta, archivo)

            if not archivo.endswith(".txt"):
                continue

            with open(ruta, "r", encoding="utf-8") as f:
                byte_offset = 0
                for linea in f:
                    linea = linea.strip()
                    if not linea:
                        continue
                    campos = linea.split("|")
                    numero_carnet = campos[0]
                    idx.write(f"{numero_carnet}|{archivo}|{byte_offset}\n")
                    byte_offset += len(linea.encode("utf-8")) + 1

def buscar_estudiante_indexado(numero_carnet, archivo_indice, carpeta):
    inicio = time.perf_counter()

    with open(archivo_indice, "r", encoding="utf-8") as idx:
        for linea in idx:
            carnet, archivo, offset = linea.strip().split("|")
            if carnet == numero_carnet:
                ruta = os.path.join(carpeta, archivo)
                with open(ruta, "r", encoding="utf-8") as f:
                    f.seek(int(offset))
                    registro = f.readline().strip()
                fin = time.perf_counter()
                return registro, (fin - inicio) * 1000

    fin = time.perf_counter()
    return None, (fin - inicio) * 1000

CARPETA_DATOS = "datos"
ARCHIVO_INDICE = "indice_estudiantes.txt"
REGISTROS_POR_ARCHIVO = 1000
TOTAL_ARCHIVOS = 5

NOMBRES = ["Ana", "Luis", "María", "Juan", "Carlos", "Sofía", "Pedro", "Laura"]
APELLIDOS = ["Pérez", "Gómez", "López", "Martínez", "Hernández", "Ramírez"]
CARRERAS = ["Ingeniería", "Medicina", "Derecho", "Arquitectura", "Economía"]

if __name__ == "__main__":
    carnet_prueba = "20210040"
    resultado, tiempo = buscar_estudiante_indexado(carnet_prueba, ARCHIVO_INDICE, CARPETA_DATOS)
    print(resultado)
    print(f"{tiempo:.4f}")