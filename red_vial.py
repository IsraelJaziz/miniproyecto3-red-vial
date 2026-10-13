import xml.etree.ElementTree as ET
from lista_enlazada import ListaEnlazada

VIAS_VALIDAS = {
    "motorway", "motorway_link", "trunk", "trunk_link",
    "primary", "primary_link", "secondary", "secondary_link",
    "tertiary", "tertiary_link", "residential", "living_street", "unclassified"
}

def cargar_red(ruta_osm):
    coordenadas = {}
    vias_finales = {}
    
    stats = {
        "nodos_totales": 0,
        "vias_totales": 0,
        "vias_validas": 0,
        "excluidas_no_vehicular": 0,
        "excluidas_restringido": 0,
        "excluidas_incompletas": 0,
        "con_sentido": 0,
        "bidireccionales": 0
    }

    
    for evento, elemento in ET.iterparse(ruta_osm, events=("end",)):
        if elemento.tag == "node":
            stats["nodos_totales"] += 1
            nid = int(elemento.attrib["id"])
            lat = float(elemento.attrib["lat"])
            lon = float(elemento.attrib["lon"])
            coordenadas[nid] = (lat, lon)
            elemento.clear() 
        elif elemento.tag == "way":
            elemento.clear()

    
    for evento, elemento in ET.iterparse(ruta_osm, events=("end",)):
        if elemento.tag == "way":
            stats["vias_totales"] += 1
            wid = int(elemento.attrib["id"])
            
            tags = {}
            for t in elemento.findall("tag"):
                tags[t.attrib["k"]] = t.attrib["v"]

            highway = tags.get("highway")
            if highway not in VIAS_VALIDAS:
                stats["excluidas_no_vehicular"] += 1
                elemento.clear()
                continue

            if tags.get("access") in ("private", "no") or tags.get("vehicle") == "no" or tags.get("motor_vehicle") == "no":
                stats["excluidas_restringido"] += 1
                elemento.clear()
                continue

            refs = [int(nd.attrib["ref"]) for nd in elemento.findall("nd")]

            if len(refs) < 2 or any(r not in coordenadas for r in refs):
                stats["excluidas_incompletas"] += 1
                elemento.clear()
                continue


            oneway = tags.get("oneway", "").strip()
            if oneway == "-1":
                refs.reverse()
                stats["con_sentido"] += 1
            elif oneway in ("yes", "1", "true"):
                stats["con_sentido"] += 1
            else:
                stats["bidireccionales"] += 1

            via = ListaEnlazada(id_via=wid)
            for r in refs:
                lat, lon = coordenadas[r]
                via.insertar_final(r, lat, lon)

            vias_finales[wid] = via
            stats["vias_validas"] += 1
            elemento.clear()

    return vias_finales, stats


def crear_indice(vias):
    indice = {}
    for wid in sorted(vias):
        actual = vias[wid].cabeza
        while actual is not None:
            nid = actual.id_nodo
            if nid not in indice:
                indice[nid] = []
            if wid not in indice[nid]:
                indice[nid].append(wid)
            actual = actual.siguiente
    return indice
