import sys
from haversine import haversine

class Nodo:
    def __init__(self, id_nodo, lat, lon):
        self.id_nodo = int(id_nodo)
        self.lat = float(lat)
        self.lon = float(lon)
        self.siguiente = None

    def __repr__(self):
        return f"Nodo({self.id_nodo})"


class ListaEnlazada:
    def __init__(self, id_via=0):
        self.id_via = int(id_via)
        self.cabeza = None
        self.cola = None  
        self.longitud = 0

    def __len__(self):
        return self.longitud

    def esta_vacia(self):
        return self.cabeza is None

    # --- INSERCIONES ---

    def insertar_inicio(self, id_nodo, lat, lon):
        nuevo = Nodo(id_nodo, lat, lon)
        if self.esta_vacia():
            self.cabeza = nuevo
            self.cola = nuevo
        else:
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo
        self.longitud += 1

    def insertar_final(self, id_nodo, lat, lon):
        nuevo = Nodo(id_nodo, lat, lon)
        if self.esta_vacia():
            self.cabeza = nuevo
            self.cola = nuevo
        else:
            self.cola.siguiente = nuevo
            self.cola = nuevo
        self.longitud += 1

    def insertar_posicion(self, indice, id_nodo, lat, lon):
        if indice < 0 or indice > self.longitud:
            raise IndexError("Indice fuera de rango")
        
        if indice == 0:
            self.insertar_inicio(id_nodo, lat, lon)
        elif indice == self.longitud:
            self.insertar_final(id_nodo, lat, lon)
        else:
            nuevo = Nodo(id_nodo, lat, lon)
            actual = self.cabeza
            # recorremos hasta llegar un nodo antes de la posicion
            for _ in range(indice - 1):
                actual = actual.siguiente
            nuevo.siguiente = actual.siguiente
            actual.siguiente = nuevo
            self.longitud += 1


    # --- ELIMINACIONES ---

    def eliminar_inicio(self):
        if self.esta_vacia():
            raise IndexError("La lista esta vacia")
        
        borrado = self.cabeza
        self.cabeza = self.cabeza.siguiente
        self.longitud -= 1
        
        if self.esta_vacia():
            self.cola = None
            
        return borrado

    def eliminar_final(self):
        if self.esta_vacia():
            raise IndexError("La lista esta vacia")
        
        if self.cabeza == self.cola:
            borrado = self.cabeza
            self.cabeza = None
            self.cola = None
            self.longitud -= 1
            return borrado

        actual = self.cabeza
        while actual.siguiente != self.cola:
            actual = actual.siguiente

        borrado = self.cola
        actual.siguiente = None
        self.cola = actual
        self.longitud -= 1
        return borrado

    def eliminar_posicion(self, indice):
        if indice < 0 or indice >= self.longitud:
            raise IndexError("Indice fuera de rango")

        if indice == 0:
            return self.eliminar_inicio()
        if indice == self.longitud - 1:
            return self.eliminar_final()

        actual = self.cabeza
        for _ in range(indice - 1):
            actual = actual.siguiente

        borrado = actual.siguiente
        actual.siguiente = borrado.siguiente
        self.longitud -= 1
        return borrado

    def eliminar_valor(self, id_nodo):
        if self.esta_vacia():
            return False

        if self.cabeza.id_nodo == id_nodo:
            self.eliminar_inicio()
            return True

        actual = self.cabeza
        while actual.siguiente and actual.siguiente.id_nodo != id_nodo:
            actual = actual.siguiente

        if actual.siguiente is None:
            return False

        if actual.siguiente == self.cola:
            self.cola = actual
            self.cola.siguiente = None
        else:
            actual.siguiente = actual.siguiente.siguiente

        self.longitud -= 1
        return True


    # --- INVERTIR ---

    def invertir(self):
        if self.longitud <= 1:
            return

        anterior = None
        actual = self.cabeza
        self.cola = self.cabeza

        while actual is not None:
            # guardamos referencia antes de romper la flecha
            sig_aux = actual.siguiente
            actual.siguiente = anterior
            anterior = actual
            actual = sig_aux

        self.cabeza = anterior


    # --- CALCULOS DE DISTANCIA ---

    def longitud_iterativa(self):
        if self.longitud < 2:
            return 0.0

        dist = 0.0
        actual = self.cabeza
        while actual.siguiente is not None:
            sig = actual.siguiente
            dist += haversine(actual.lat, actual.lon, sig.lat, sig.lon)
            actual = sig
        return dist

    def longitud_recursiva(self):
        if self.longitud < 2:
            return 0.0

        if self.longitud > (sys.getrecursionlimit() - 50):
            raise RecursionError("Demasiados nodos para usar recursion")

        def _recorrer(nodo):
            if nodo is None or nodo.siguiente is None:
                return 0.0
            tramo = haversine(nodo.lat, nodo.lon, nodo.siguiente.lat, nodo.siguiente.lon)
            return tramo + _recorrer(nodo.siguiente)

        return _recorrer(self.cabeza)


    # --- UTILIDADES ---

    def obtener_ids(self):
        ids = []
        actual = self.cabeza
        while actual is not None:
            ids.append(actual.id_nodo)
            actual = actual.siguiente
        return ids