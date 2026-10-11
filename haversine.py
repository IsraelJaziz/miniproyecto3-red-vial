"""Funciones auxiliares para el Miniproyecto 3.

La función haversine calcula la distancia de gran círculo entre dos
coordenadas geográficas expresadas en grados decimales.
"""

from math import radians, sin, cos, sqrt, atan2

RADIO_TIERRA_M = 6_371_000


def haversine(lat1, lon1, lat2, lon2):
    """Devuelve la distancia Haversine entre dos puntos, en metros.

    Parámetros:
        lat1, lon1: latitud y longitud del primer punto, en grados.
        lat2, lon2: latitud y longitud del segundo punto, en grados.

    No realiza redondeo del resultado.
    """
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)

    a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return RADIO_TIERRA_M * c


if __name__ == "__main__":
    # Ejemplo ficticio mínimo.
    d = haversine(18.8500, -97.1050, 18.8510, -97.1040)
    print(f"Distancia: {d:.2f} m")
