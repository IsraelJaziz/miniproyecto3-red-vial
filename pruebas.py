import os
import random
import tempfile
from haversine import haversine
from intersecciones import detectar_intersecciones
from lista_enlazada import ListaEnlazada
from red_vial import cargar_red, crear_indice
from secuencia_contigua import SecuenciaLista

RUTA = "red_vial_orizaba_centro.osm"


def crear_lista(ids):
    lista = ListaEnlazada()
    for i in ids:
        lista.insertar_final(i, 18.85, -97.10)
    return lista


def esta_bien_armada(lista):
    contados = 0
    ultimo = None
    actual = lista.cabeza
    while actual is not None:
        contados += 1
        ultimo = actual
        actual = actual.siguiente
        assert contados <= lista.longitud + 1, "parece que hay un ciclo"
    return contados == lista.longitud and ultimo is lista.cola


def prueba_lista_vacia():
    lista = ListaEnlazada()
    assert lista.esta_vacia()
    assert lista.longitud == 0
    assert lista.obtener_ids() == []
    assert lista.longitud_iterativa() == 0.0


def prueba_insertar_inicio_medio_final():
    lista = crear_lista([1, 2, 3])
    lista.insertar_inicio(0, 18.85, -97.10)
    lista.insertar_posicion(2, 99, 18.85, -97.10)
    lista.insertar_posicion(5, 4, 18.85, -97.10)
    assert lista.obtener_ids() == [0, 1, 99, 2, 3, 4]
    assert lista.longitud == 6
    assert esta_bien_armada(lista)


def prueba_insertar_en_lista_vacia():
    lista = ListaEnlazada()
    lista.insertar_posicion(0, 7, 18.85, -97.10)
    assert lista.obtener_ids() == [7]
    assert lista.cabeza is lista.cola


def prueba_insertar_posicion_invalida():
    lista = crear_lista([1, 2])
    for indice in (3, -1):
        try:
            lista.insertar_posicion(indice, 9, 18.85, -97.10)
            assert False, "debio lanzar IndexError"
        except IndexError:
            pass
    assert lista.obtener_ids() == [1, 2]


def prueba_eliminar_inicio_medio_final():
    lista = crear_lista([1, 2, 3, 4, 5])
    assert lista.eliminar_inicio().id_nodo == 1
    assert lista.eliminar_posicion(1).id_nodo == 3
    assert lista.eliminar_final().id_nodo == 5
    assert lista.obtener_ids() == [2, 4]
    assert lista.longitud == 2
    assert esta_bien_armada(lista)


def prueba_eliminar_posicion_en_los_extremos():
    lista = crear_lista([1, 2, 3])
    assert lista.eliminar_posicion(2).id_nodo == 3
    assert lista.eliminar_posicion(0).id_nodo == 1
    assert lista.obtener_ids() == [2]
    assert esta_bien_armada(lista)


def prueba_eliminar_hasta_vaciar():
    lista = crear_lista([7])
    lista.eliminar_final()
    assert lista.longitud == 0
    assert lista.cabeza is None and lista.cola is None
    otra = crear_lista([7])
    otra.eliminar_inicio()
    assert otra.cabeza is None and otra.cola is None


def prueba_eliminar_en_lista_vacia_o_fuera_de_rango():
    vacia = ListaEnlazada()
    for operacion in (vacia.eliminar_inicio, vacia.eliminar_final):
        try:
            operacion()
            assert False, "debio lanzar IndexError"
        except IndexError:
            pass
    lista = crear_lista([1])
    for indice in (1, -1):
        try:
            lista.eliminar_posicion(indice)
            assert False, "debio lanzar IndexError"
        except IndexError:
            pass


def prueba_cola_se_actualiza():
    lista = crear_lista([1, 2, 3])
    lista.eliminar_final()
    lista.insertar_final(7, 18.85, -97.10)
    assert lista.obtener_ids() == [1, 2, 7]
    assert esta_bien_armada(lista)


def prueba_eliminar_valor():
    lista = crear_lista([1, 2, 3, 2])
    assert lista.eliminar_valor(2) is True
    assert lista.obtener_ids() == [1, 3, 2]
    assert lista.eliminar_valor(2) is True
    assert lista.eliminar_valor(2) is False
    assert lista.eliminar_valor(1) is True
    assert lista.obtener_ids() == [3]
    assert esta_bien_armada(lista)
    assert ListaEnlazada().eliminar_valor(1) is False


def prueba_invertir():
    lista = crear_lista([1, 2, 3, 4])
    lista.invertir()
    assert lista.obtener_ids() == [4, 3, 2, 1]
    assert esta_bien_armada(lista)
    lista.insertar_final(0, 18.85, -97.10)
    assert lista.obtener_ids() == [4, 3, 2, 1, 0]
    vacia = ListaEnlazada()
    vacia.invertir()
    assert vacia.obtener_ids() == []
    una = crear_lista([5])
    una.invertir()
    assert una.obtener_ids() == [5]


def prueba_contra_list_de_python():
    azar = random.Random(7)
    lista = ListaEnlazada()
    referencia = []
    for _ in range(1500):
        if len(referencia) > 0 and azar.random() < 0.4:
            indice = azar.randrange(len(referencia))
            assert lista.eliminar_posicion(indice).id_nodo == referencia.pop(indice)
        else:
            indice = azar.randint(0, len(referencia))
            valor = azar.randint(0, 999999)
            lista.insertar_posicion(indice, valor, 18.85, -97.10)
            referencia.insert(indice, valor)
    assert lista.obtener_ids() == referencia
    assert esta_bien_armada(lista)


# ---------------------------------------------------------------
# Longitud: ciclo y recursion
# ---------------------------------------------------------------
def prueba_longitud_conocida():
    lista = ListaEnlazada()
    lista.insertar_final(1, 0.0, 0.0)
    lista.insertar_final(2, 1.0, 0.0)
    assert abs(lista.longitud_iterativa() - 111194.92664455874) < 1e-6
    assert abs(lista.longitud_recursiva() - 111194.92664455874) < 1e-6


def prueba_longitud_recursiva_igual_al_ciclo():
    lista = ListaEnlazada()
    puntos = [(1, 18.850, -97.110), (2, 18.851, -97.109), (3, 18.852, -97.108), (4, 18.853, -97.1075)]
    for p in puntos:
        lista.insertar_final(p[0], p[1], p[2])
    assert lista.longitud_iterativa() == lista.longitud_recursiva()
    assert ListaEnlazada().longitud_recursiva() == 0.0
    una = ListaEnlazada()
    una.insertar_final(1, 18.85, -97.10)
    assert una.longitud_recursiva() == 0.0


def prueba_recursion_muy_larga_da_error_claro():
    lista = ListaEnlazada()
    for i in range(1000):
        lista.insertar_final(i, 18.85 + i * 0.00001, -97.10)
    try:
        lista.longitud_recursiva()
        assert False, "debio lanzar RecursionError"
    except RecursionError:
        pass
    assert lista.longitud_iterativa() > 0


def prueba_secuencia_lista_da_lo_mismo_que_la_enlazada():
    azar = random.Random(3)
    enlazada = ListaEnlazada()
    contigua = SecuenciaLista()
    for i in range(300):
        lat = 18.84 + azar.random() * 0.01
        lon = -97.12 + azar.random() * 0.02
        enlazada.insertar_final(i, lat, lon)
        contigua.insertar_final(i, lat, lon)
    for _ in range(200):
        if len(contigua) > 1 and azar.random() < 0.5:
            indice = azar.randrange(len(contigua))
            enlazada.eliminar_posicion(indice)
            contigua.eliminar_posicion(indice)
        else:
            indice = azar.randint(0, len(contigua))
            enlazada.insertar_posicion(indice, 10000 + indice, 18.85, -97.10)
            contigua.insertar_posicion(indice, 10000 + indice, 18.85, -97.10)
    assert enlazada.obtener_ids() == contigua.obtener_ids()
    assert abs(enlazada.longitud_iterativa() - contigua.longitud_iterativa()) < 1e-6
    try:
        contigua.insertar_posicion(len(contigua) + 1, 1, 18.85, -97.10)
        assert False, "debio lanzar IndexError"
    except IndexError:
        pass


def prueba_haversine():
    assert abs(haversine(0, 0, 1, 0) - 111194.92664455874) < 1e-6
    assert haversine(18.85, -97.1, 18.85, -97.1) == 0.0
    assert abs(haversine(18.8500, -97.1050, 18.8510, -97.1040) - 153.0943) < 1e-3
    ida = haversine(18.85, -97.11, 18.84, -97.10)
    vuelta = haversine(18.84, -97.10, 18.85, -97.11)
    assert abs(ida - vuelta) < 1e-9


def prueba_intersecciones():
    vias = {100: [1, 2, 3, 4], 200: [5, 2, 6], 300: [7, 3, 8]}
    assert detectar_intersecciones(vias) == {2: [100, 200], 3: [100, 300]}
    assert detectar_intersecciones({1: [5, 6, 5], 2: [9, 8]}) == {}


XML_PEQUENO = """<osm>
  <node id="1" lat="18.850" lon="-97.110"/>
  <node id="2" lat="18.851" lon="-97.110"/>
  <node id="3" lat="18.852" lon="-97.110"/>
  <node id="4" lat="18.853" lon="-97.110"/>
  <way id="10"><nd ref="1"/><nd ref="2"/><nd ref="3"/><tag k="highway" v="residential"/></way>
  <way id="11"><nd ref="1"/><nd ref="2"/><nd ref="3"/><tag k="highway" v="residential"/><tag k="oneway" v="-1"/></way>
  <way id="12"><nd ref="2"/><nd ref="4"/><tag k="highway" v="primary"/><tag k="oneway" v="yes"/></way>
  <way id="13"><nd ref="1"/><nd ref="2"/><tag k="highway" v="service"/></way>
  <way id="14"><nd ref="1"/><nd ref="2"/><tag k="highway" v="residential"/><tag k="access" v="private"/></way>
  <way id="15"><nd ref="1"/><nd ref="2"/><tag k="highway" v="residential"/><tag k="motor_vehicle" v="no"/></way>
  <way id="16"><nd ref="1"/><nd ref="999"/><tag k="highway" v="residential"/></way>
  <way id="17"><nd ref="1"/><tag k="highway" v="residential"/></way>
  <way id="18"><nd ref="3"/><nd ref="4"/><tag k="highway" v="residential"/><tag k="oneway" v="no"/></way>
  <way id="19"><nd ref="3"/><nd ref="4"/></way>
</osm>"""


def cargar_xml_pequeno():
    with tempfile.TemporaryDirectory() as carpeta:
        ruta = os.path.join(carpeta, "pequeno.osm")
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(XML_PEQUENO)
        return cargar_red(ruta)


def prueba_filtrado_con_xml_pequeno():
    vias, stats = cargar_xml_pequeno()
    assert sorted(vias) == [10, 11, 12, 18]
    assert stats["nodos_totales"] == 4
    assert stats["vias_totales"] == 10
    assert stats["vias_validas"] == 4
    assert stats["excluidas_no_vehicular"] == 2
    assert stats["excluidas_restringido"] == 2
    assert stats["excluidas_incompletas"] == 2


def prueba_sentido_con_xml_pequeno():
    vias, stats = cargar_xml_pequeno()
    assert vias[10].obtener_ids() == [1, 2, 3]
    assert vias[11].obtener_ids() == [3, 2, 1]
    assert vias[12].obtener_ids() == [2, 4]
    assert vias[18].obtener_ids() == [3, 4]
    assert stats["con_sentido"] == 2
    assert stats["bidireccionales"] == 2


def prueba_indice_e_intersecciones_con_xml_pequeno():
    vias, _ = cargar_xml_pequeno()
    indice = crear_indice(vias)
    assert indice[2] == [10, 11, 12]
    assert indice[4] == [12, 18]
    assert 424242 not in indice
    ids = {}
    for wid in vias:
        ids[wid] = vias[wid].obtener_ids()
    assert detectar_intersecciones(ids) == {1: [10, 11], 2: [10, 11, 12], 3: [10, 11, 18], 4: [12, 18]}


def prueba_nodo_repetido_en_la_misma_via_cuenta_una_vez():
    vias = {20: crear_lista([1, 2, 3, 1]), 30: crear_lista([3, 4])}
    indice = crear_indice(vias)
    assert indice[1] == [20]
    assert indice[3] == [20, 30]
    assert detectar_intersecciones({20: [1, 2, 3, 1], 30: [3, 4]}) == {3: [20, 30]}


def prueba_archivo_oficial():
    vias, stats = cargar_red(RUTA)
    assert stats["nodos_totales"] == 8741
    assert stats["vias_totales"] == 1874
    assert stats["vias_validas"] == 355
    assert stats["excluidas_no_vehicular"] == 1513
    assert stats["excluidas_restringido"] == 6
    assert stats["excluidas_incompletas"] == 0
    assert stats["con_sentido"] == 181
    assert stats["bidireccionales"] == 174

    ids = {}
    for wid in vias:
        ids[wid] = vias[wid].obtener_ids()
    assert len(detectar_intersecciones(ids)) == 453

    calle = vias[892777216]
    assert calle.longitud == 36
    assert abs(calle.longitud_iterativa() - 1634.184445639146) < 1e-6
    assert calle.longitud_iterativa() == calle.longitud_recursiva()
    assert crear_indice(vias)[462839773] == [499745924, 892044339]


PRUEBAS = [
    prueba_lista_vacia, prueba_insertar_inicio_medio_final, prueba_insertar_en_lista_vacia,
    prueba_insertar_posicion_invalida, prueba_eliminar_inicio_medio_final,
    prueba_eliminar_posicion_en_los_extremos, prueba_eliminar_hasta_vaciar,
    prueba_eliminar_en_lista_vacia_o_fuera_de_rango, prueba_cola_se_actualiza,
    prueba_eliminar_valor, prueba_invertir, prueba_contra_list_de_python,
    prueba_longitud_conocida, prueba_longitud_recursiva_igual_al_ciclo,
    prueba_recursion_muy_larga_da_error_claro,
    prueba_secuencia_lista_da_lo_mismo_que_la_enlazada,
    prueba_haversine, prueba_intersecciones,
    prueba_filtrado_con_xml_pequeno, prueba_sentido_con_xml_pequeno,
    prueba_indice_e_intersecciones_con_xml_pequeno,
    prueba_nodo_repetido_en_la_misma_via_cuenta_una_vez,
    prueba_archivo_oficial,
]

if __name__ == "__main__":
    for prueba in PRUEBAS:
        prueba()
        print("OK  ", prueba.__name__)
    print("\nTodas las pruebas pasaron:", len(PRUEBAS))
