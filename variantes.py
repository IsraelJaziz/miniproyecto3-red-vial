from haversine import haversine

class NodoDoble:
    def __init__(self, id_nodo, lat, lon):
        self.id_nodo = int(id_nodo)
        self.lat = float(lat)
        self.lon = float(lon)
        self.siguiente = None
        self.anterior = None  # la unica diferencia, flecha hacia atras


class ListaDoble:
    def __init__(self, id_via=0):
        self.id_via = id_via
        self.cabeza = None
        self.cola = None
        self.longitud = 0

    # --- INSERCION DOBLE ---

    def insertar_final(self, id_nodo, lat, lon):
        nuevo = NodoDoble(id_nodo, lat, lon)
        if self.cabeza is None:
            self.cabeza = nuevo
            self.cola = nuevo
        else:
            self.cola.siguiente = nuevo
            nuevo.anterior = self.cola
            self.cola = nuevo
        self.longitud += 1


class NodoCircular:
    def __init__(self, id_nodo, lat, lon):
        self.id_nodo = int(id_nodo)
        self.lat = float(lat)
        self.lon = float(lon)
        self.siguiente = None


class ListaCircular:
    def __init__(self, id_via=0):
        self.id_via = id_via
        self.cabeza = None
        self.cola = None
        self.longitud = 0

    # --- INSERCION CIRCULAR ---

    def insertar_final(self, id_nodo, lat, lon):
        nuevo = NodoCircular(id_nodo, lat, lon)
        if self.cabeza is None:
            self.cabeza = nuevo
            self.cola = nuevo
            nuevo.siguiente = self.cabeza  # se muerde la cola
        else:
            self.cola.siguiente = nuevo
            self.cola = nuevo
            self.cola.siguiente = self.cabeza  # se actualiza el cierre
        self.longitud += 1

    # --- CALCULO CIRCULAR ---

    def calcular_longitud(self):
        if self.longitud < 2:
            return 0.0

        dist = 0.0
        actual = self.cabeza
        pasos = 0

        # usamos contador (longitud - 1) para no dar vueltas al infinito
        while pasos < self.longitud - 1:
            sig = actual.siguiente
            dist += haversine(actual.lat, actual.lon, sig.lat, sig.lon)
            actual = sig
            pasos += 1

        return dist