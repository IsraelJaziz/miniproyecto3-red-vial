from red_vial import cargar_red, crear_indice
from intersecciones import detectar_intersecciones

def main():
    ruta = "red_vial_orizaba_centro.osm"
    way_oficial = 892777216

    print("\nIniciando carga de red vial...")
    vias, stats = cargar_red(ruta)

    print("\n--- Problema 1: Limpieza ---")
    for clave, valor in stats.items():
        print(f"{clave}: {valor}")

    if way_oficial not in vias:
        print("Error: No se encontro la via de control.")
        return

    calle = vias[way_oficial]

    print("\n--- Problema 2: Distancias ---")
    print(f"Way ID: {way_oficial}")
    print(f"Nodos: {calle.longitud}")
    print(f"Dist iterativa: {calle.longitud_iterativa()} m")
    print(f"Dist recursiva: {calle.longitud_recursiva()} m")

    print("\n--- Problema 3: Intersecciones y vias por nodo ---")
    diccionario_vias = {}
    for wid, via in vias.items():
        diccionario_vias[wid] = via.obtener_ids()

    intersecciones = detectar_intersecciones(diccionario_vias)
    print(f"Total intersecciones: {len(intersecciones)}")

    indice = crear_indice(vias)

    nodo_cruce = 462839773
    print(f"Nodo {nodo_cruce} pasa por las vias: {indice.get(nodo_cruce, [])}")

    nodo_ejemplo = calle.cabeza.siguiente.id_nodo
    print(f"Nodo {nodo_ejemplo} pasa por las vias: {indice.get(nodo_ejemplo, [])}")

if __name__ == "__main__":
    main()
