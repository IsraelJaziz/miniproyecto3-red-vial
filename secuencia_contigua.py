from haversine import haversine

class SecuenciaLista:
    def __init__(self, datos=None):
        self.datos = []
        if datos is not None:
            self.datos = list(datos)

    def __len__(self):
        return len(self.datos)

    def copiar(self):
        return SecuenciaLista(self.datos)

    def obtener_ids(self):
        ids = []
        for dato in self.datos:
            ids.append(dato[0])
        return ids

    def insertar_inicio(self, id_nodo, lat, lon):
        self.datos.insert(0, (id_nodo, lat, lon))

    def insertar_final(self, id_nodo, lat, lon):
        self.datos.append((id_nodo, lat, lon))

    def insertar_posicion(self, indice, id_nodo, lat, lon):
        if indice < 0 or indice > len(self.datos):
            raise IndexError("Indice fuera de rango")
        self.datos.insert(indice, (id_nodo, lat, lon))

    def eliminar_inicio(self):
        if not self.datos:
            raise IndexError("Lista vacia")
        return self.datos.pop(0)

    def eliminar_final(self):
        if not self.datos:
            raise IndexError("Lista vacia")
        return self.datos.pop()

    def eliminar_posicion(self, indice):
        if indice < 0 or indice >= len(self.datos):
            raise IndexError("Indice fuera de rango")
        return self.datos.pop(indice)

    def longitud_iterativa(self):
        if len(self.datos) < 2:
            return 0.0

        dist = 0.0
        for i in range(len(self.datos) - 1):
            nodo_actual = self.datos[i]
            nodo_siguiente = self.datos[i + 1]
            dist += haversine(nodo_actual[1], nodo_actual[2], nodo_siguiente[1], nodo_siguiente[2])

        return dist
