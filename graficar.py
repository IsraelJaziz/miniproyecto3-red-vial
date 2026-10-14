import csv
import matplotlib.pyplot as plt

RUTA_CSV = "resultados_mediciones.csv"
RUTA_PNG = "grafica_mediciones.png"

OPERACIONES = [
    "recorrido", "longitud",
    "insertar inicio", "insertar medio", "insertar final",
    "eliminar inicio", "eliminar medio", "eliminar final",
]

def leer_csv(ruta):
    datos = {}
    with open(ruta, encoding="utf-8") as archivo:
        for fila in csv.DictReader(archivo):
            op = fila["operacion"]
            if op not in datos:
                datos[op] = {"n": [], "enlazada": [], "list": []}
            datos[op]["n"].append(int(fila["n"]))
            datos[op]["enlazada"].append(int(fila["mediana_enlazada_ns"]) / 1000)
            datos[op]["list"].append(int(fila["mediana_list_ns"]) / 1000)
    return datos

def marcas_y(minimo, maximo):
    marcas = []
    for k in range(-2, 6):
        for factor in (1, 2, 5):
            valor = factor * 10 ** k
            if minimo / 1.5 <= valor <= maximo * 1.5:
                marcas.append(valor)
    return marcas

def main():
    try:
        datos = leer_csv(RUTA_CSV)
    except FileNotFoundError:
        print("No encuentro", RUTA_CSV, "- primero corre medir.py")
        return

    fig, ejes = plt.subplots(2, 4, figsize=(14, 7))
    fig.suptitle("Lista enlazada vs list de Python (mediana de 31 repeticiones, escala log-log)")

    for ax, op in zip(ejes.flat, OPERACIONES):
        n = datos[op]["n"]
        ax.plot(n, datos[op]["enlazada"], marker="o", color="#2a78d6", label="Lista enlazada")
        ax.plot(n, datos[op]["list"], marker="o", color="#eb6834", label="list de Python")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.minorticks_off()
        ax.set_xticks(n)
        ax.set_xticklabels([str(x) for x in n])

        todos = datos[op]["enlazada"] + datos[op]["list"]
        marcas = marcas_y(min(todos), max(todos))
        ax.set_yticks(marcas)
        ax.set_yticklabels([f"{m:g}" for m in marcas])

        ax.set_title(op)
        ax.set_xlabel("nodos (n)")
        ax.set_ylabel("tiempo (microsegundos)")
        ax.grid(True, color="#e1e0d9")

    ejes[0][0].legend()
    fig.tight_layout()
    fig.savefig(RUTA_PNG, dpi=120)
    print("Grafica guardada en", RUTA_PNG)

if __name__ == "__main__":
    main()
