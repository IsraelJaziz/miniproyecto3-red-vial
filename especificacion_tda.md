# Especificación de los TDA

Miniproyecto 3 · Planificador de rutas sobre la red vial urbana · Zona Centro de Orizaba

## 1. TDA ListaEnlazada (Secuencia de nodos de una vía)

**Definición:** Almacena la secuencia ordenada de nodos que conforman una via vehicular. Cada elemento (nodo) contiene un `id_nodo` (entero), coordenadas `lat` y `lon` (decimales en grados) y una referencia al `siguiente` nodo.

**Representación:** Se implementa mediante una estructura enlazada simple con objetos y referencias definidas por el equipo y la clase principal mantiene referencias a `cabeza` (primer nodo), `cola` (ultimo nodo) y un contador de `longitud`

**Invariantes del TDA:**
- Si la estructura está vacía, `cabeza` y `cola` son nulos y `longitud` es 0
- El recorrido desde `cabeza` mediante la referencia `siguiente` termina en un valor nulo, visitando exactamente la cantidad de nodos indicada por `longitud`.
- El último nodo visitado es siempre el referenciado por `cola`.
- Las posiciones lógicas inician en 0
- La estructura es lineal (ya que no contiene ciclos)

### Operaciones y Complejidad Esperada

| Operación | Precondición | Poscondición | Complejidad |
|---|---|---|---|
| `esta_vacia()` | Ninguna | Devuelve `True` si la estructura carece de elementos | O(1) |
| `insertar_inicio(id, lat, lon)` | Ninguna | Se inserta un nuevo nodo en la posición 0; `longitud` se incrementa en 1 | O(1) |
| `insertar_final(id, lat, lon)` | Ninguna | Se inserta un nuevo nodo tras la `cola` actual; `cola` se actualiza; `longitud` se incrementa | O(1) |
| `insertar_posicion(i, id, lat, lon)` | 0 ≤ i ≤ longitud | Se inserta un nuevo nodo en la posición `i`, desplazando los subsecuentes | O(i) → Peor caso O(n) |
| `eliminar_inicio()` | La lista no está vacía | Se elimina y retorna el nodo en la posición 0; `longitud` decrece en 1 | O(1) |
| `eliminar_final()` | La lista no está vacía | Se elimina y retorna el nodo referenciado por `cola`; `cola` se actualiza al penúltimo | O(n) |
| `eliminar_posicion(i)` | 0 ≤ i < longitud | Se elimina y retorna el nodo en la posición `i` | O(i) → Peor caso O(n) |
| `eliminar_valor(id)` | Ninguna | Elimina la primera ocurrencia del `id_nodo` y devuelve `True` (o `False` si no existe) | O(n) |
| `invertir()` | Ninguna | Se invierte el orden lógico de los elementos reasignando referencias en sitio | O(n) |
| `obtener_ids()` | Ninguna | Retorna un arreglo secuencial nativo con los identificadores en orden | O(n) |
| `longitud_iterativa()` | Ninguna | Retorna la sumatoria de las distancias de haversine entre nodos consecutivos en metros | O(n) |
| `longitud_recursiva()` | La `longitud` no excede el límite máximo de recursión de python | Retorna la distancia total de la vía resolviendo el cálculo mediante llamadas recursivas | O(n) tiempo y espacio |

**Manejo de Errores:** Se lanza `IndexError` si no se cumplen las precondiciones de posición (p. ej., eliminar en lista vacía o índices inválidos) y se lanza `RecursionError` si se excede la profundidad de pila

## 2. Estructura de Control: SecuenciaLista (Arreglo Contiguo)

Para cumplir con la rúbrica se especifica un TDA que funciona como envoltura de una lista nativa de python (`list`) exponiendo los mismos métodos de inserción, eliminacion, recorrido y longitud iterativa que `ListaEnlazada`, con las mismas validaciones de rango

| Operación | Complejidad Teórica Esperada |
|---|---|
| `insertar_inicio`, `eliminar_inicio` | O(n) por reubicación de elementos contiguos |
| `insertar_final`, `eliminar_final` | O(1) amortizado |
| `insertar_posicion`, `eliminar_posicion` | O(n) |
| `obtener_ids`, `longitud_iterativa` | O(n) |

## 3. Estructuras Auxiliares del Sistema

Para gestionar la red a nivel macro el sistema utiliza diccionarios de python que ofrecen acceso en tiempo esperado O(1)

| Estructura | Propósito en el diseño |
|---|---|
| `coordenadas` | Diccionario `{id_nodo: (lat, lon)}` para almacenar temporalmente los nodos crudos durante la primera pasada de lectura |
| `vias` | Diccionario `{id_via: ListaEnlazada}` que almacena el grafo resultante tras aplicar las reglas de filtrado de OpenStreetMap |
| `indice` | Diccionario `{id_nodo: [id_via, ...]}` para localizar en qué vías vehiculares participa un nodo dado (resolución del Problema 3) |

## 4. Criterios de Dominio (Reglas de la Red Vial)

La carga del archivo XML y la instanciación de los TDA se rige por las siguientes reglas de negocio antes de operar sobre la red:
1. **Filtro vehicular:** Solo se instancian listas para elementos con etiqueta `highway` vehicular válida (`motorway`, `trunk`, `primary`, `secondary`, `tertiary` y derivados `_link`, `residential`, `living_street`, `unclassified`)
2. **Filtro de acceso:** Se descartan vias con etiquetas de restricción `access=private/no` o `vehicle/motor_vehicle=no`.
3. **Integridad:** Una lista enlazada debe contener al menos 2 nodos válidos para existir
4. **Sentido de circulación (`oneway`):** Se respeta el orden de insercion si es `yes/1/true`; se invierte la secuencia de referencias con `reverse()` antes de construir la lista enlazada si es `-1`.
5. **Métrica de distancia:** El calculo de longitud consume la función de haversine asumiendo un radio terrestre R = 6,371,000 m, sin redondeos intermedios