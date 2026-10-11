"""Función auxiliar para detectar intersecciones entre vías procesadas.

Contrato de intercambio:
    entrada  -> {way_id: [node_id, node_id, ...], ...}
    salida   -> {node_id: [way_id, way_id, ...], ...}

La función supone que las vías ya fueron cargadas y filtradas correctamente
por el estudiante. No corrige ni limpia los datos de entrada.
"""


def detectar_intersecciones(vias):
    """Devuelve nodos compartidos por dos o más way_id distintos.

    Los node_id y way_id se tratan como enteros. Cada way_id cuenta una sola
    vez por nodo, aunque el nodo se repita dentro de la misma vía. La salida
    queda ordenada ascendentemente para facilitar resultados reproducibles.
    """
    usos = {}

    for way_id in sorted(vias):
        for node_id in set(vias[way_id]):
            usos.setdefault(node_id, set()).add(way_id)

    resultado = {}
    for node_id in sorted(usos):
        way_ids = sorted(usos[node_id])
        if len(way_ids) >= 2:
            resultado[node_id] = way_ids

    return resultado


if __name__ == "__main__":
    # Ejemplo ficticio mínimo.
    vias = {
        100: [1, 2, 3, 4],
        200: [5, 2, 6],
        300: [7, 3, 8],
    }
    print(detectar_intersecciones(vias))