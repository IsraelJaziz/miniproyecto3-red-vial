import time
import statistics
from red_vial import cargar_red
from lista_enlazada import ListaEnlazada
from secuencia_contigua import SecuenciaLista

RUTA = "red_vial_orizaba_centro.osm"
WAY_ID = 892777216
REPETICIONES = 31
TAMANOS_EXTRA = [1000, 10000, 100000]
NUEVO = (999999, 18.85, -97.10)

def clonar_lista(lista_original):
    copia = ListaEnlazada()
    actual = lista_original.cabeza
    while actual is not None:
        copia.insertar_final(actual.id_nodo, actual.lat, actual.lon)
        actual = actual.siguiente
    return copia

def lista_a_datos(lista):
    datos = []
    actual = lista.cabeza
    while actual is not None:
        datos.append((actual.id_nodo, actual.lat, actual.lon))
        actual = actual.siguiente
    return datos

def crear_datos_inventados(n):
    datos = []
    for i in range(n):
        lat = 18.84 + (i % 1000) * 0.000017
        lon = -97.12 + (i // 1000) * 0.00002
        datos.append((10**12 + i, lat, lon))
    return datos

def medir(preparar, operacion):
    tiempos = []
    for _ in range(REPETICIONES):
        estructura = preparar()
        inicio = time.perf_counter_ns()
        operacion(estructura)
        fin = time.perf_counter_ns()

        tiempos.append(fin - inicio)
    return statistics.median(tiempos)

def main():
    print("Cargando el mapa...")
    vias, _ = cargar_red(RUTA)
    calle_original = vias[WAY_ID]

    conjuntos = [(calle_original.longitud, lista_a_datos(calle_original))]
    for n in TAMANOS_EXTRA:
        conjuntos.append((n, crear_datos_inventados(n)))

    filas_csv = ["n,operacion,mediana_enlazada_ns,mediana_list_ns"]

    for n, datos in conjuntos:
        mitad = n // 2

        original = ListaEnlazada()
        for d in datos:
            original.insertar_final(d[0], d[1], d[2])

        operaciones = [
            ("recorrido",       lambda e: e.obtener_ids()),
            ("longitud",        lambda e: e.longitud_iterativa()),
            ("insertar inicio", lambda e: e.insertar_inicio(NUEVO[0], NUEVO[1], NUEVO[2])),
            ("insertar medio",  lambda e: e.insertar_posicion(mitad, NUEVO[0], NUEVO[1], NUEVO[2])),
            ("insertar final",  lambda e: e.insertar_final(NUEVO[0], NUEVO[1], NUEVO[2])),
            ("eliminar inicio", lambda e: e.eliminar_inicio()),
            ("eliminar medio",  lambda e: e.eliminar_posicion(mitad)),
            ("eliminar final",  lambda e: e.eliminar_final()),
        ]

        print(f"\nn = {n} nodos (mediana en microsegundos)")
        print(f"{'operacion':<17}{'enlazada':>12}{'list':>12}")
        print("-" * 41)

        for nombre, operacion in operaciones:
            t_enlazada = medir(lambda: clonar_lista(original), operacion)
            t_list = medir(lambda: SecuenciaLista(datos), operacion)
            print(f"{nombre:<17}{t_enlazada / 1000:>12.1f}{t_list / 1000:>12.1f}")
            filas_csv.append(f"{n},{nombre},{int(t_enlazada)},{int(t_list)}")

    with open("resultados_mediciones.csv", "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(filas_csv) + "\n")
    print("\nGuardado en resultados_mediciones.csv")

if __name__ == "__main__":
    main()
