# Planificador de rutas sobre la red vial urbana — Reporte técnico

Estructuras de Datos · Ingeniería en Ciencia de Datos · TecNM / Instituto Tecnológico de Orizaba
Catedrático: Dr. Ulises Juárez Martínez · Zona Centro de Orizaba (≈ 4.02 km²) · Entrega: 15 de octubre de 2026
Integrantes: Díaz Bello Israel Jaziz, Miranda Chávez Gabriela, Pérez Virgen Emiliano

## 1. Análisis del problema

El programa modela la red de calles del centro de Orizaba leyendo el archivo `red_vial_orizaba_centro.osm`. Cada calle (`way`) es una secuencia de nodos con coordenadas geográficas (`lat`, `lon`). Por ende tuvimos que resolver cuatro cosas:

1. Guardar la secuencia de nodos de cada calle para poder insertar y borrar posiciones.
2. Calcular cuánto mide la calle completa usando la fórmula de haversine (con ciclos y recursividad).
3. Encontrar rapidamente todas las calles que cruzan por un nodo en específico.
4. Comparar qué es mas rápido: si usar nuestra lista de punteros o una lista normal de Python.

**Sobre los datos:** El mapa original tiene 1,874 registros pero después de quitar parques y vias cerradas, nos quedaron **355 vías válidas** para autos y un dato muy importante es que las calles reales de Orizaba son cortas: la mayoría tiene unos 3 nodos y la calle más larga es Norte 2 (`892777216`) con **36 nodos**

## 2. Los TDA (Estructuras que usamos)

Toda la explicación detallada de complejidad está en `docs/especificacion_tda.md`. Usamos:

- **`ListaEnlazada` (`lista_enlazada.py`):** Es la estructura basada en punteros. Tiene `cabeza`, `cola` y `longitud`. Cuenta con todas las operaciones de insertar, eliminar, invertir y calcular distancias
- **`SecuenciaLista` (`secuencia_contigua.py`):** Es solo un envoltorio para una `list` nativa de Python. La usamos únicamente para poder comparar los tiempos en el Problema 4 de forma justa
- **Diccionarios (`red_vial.py`):** Usamos un diccionario para guardar toda la red de calles cargadas y otro (`crear_indice`) para guardar que calles pasan por cada cruce

## 3. Limpieza del archivo y resultados

Para que la memoria no se trabara el programa lee el XML en dos partes con `xml.etree.ElementTree.iterparse`. Primero guarda todos los nodos y luego arma las calles filtrandolas y una regla clave fue que si una calle tenía `oneway=-1` (que significa que en el mapa se dibujo al reves) se volteo su lista de IDs en Python antes de crear la lista enlazada

| Concepto | Resultado obtenido |
|---|---|
| Total de nodos / ways en el archivo `.osm` | 8,741 nodos / 1,874 ways |
| Vías descartadas (parques, edificios o sin etiqueta) | 1,513 |
| Vías descartadas por decir acceso privado | 6 |
| **Vías vehiculares válidas** | **355** (181 con un sentido, 174 bidireccionales) |
| Nodos distintos en esas 355 vías | 1,127 |
| **Intersecciones detectadas** (cruces) | **453** |
| Longitud de Norte 2 (36 nodos) — Iterativa | **1,634.1844456391464 m** |
| Longitud de Norte 2 (36 nodos) — Recursiva | **1,634.1844456391464 m** |
| Vías que pasan por el nodo `462839773` | `[499745924, 892044339]` |
| Verificación base del profesor (1° de latitud) | 111,194.93 m |

## 4. Respuesta a la pregunta guía

*¿Qué representación nos conviene más para guardar los nodos y por qué?*

Al ver nuestras graficas de tiempos supimos de que depende de lo que quieras hacer:

- **Para insertar al inicio o al final:** Nuestra `ListaEnlazada` gana por mucho porque como tenemos los punteros `cabeza` y `cola`, insertar toma tiempo O(1). En la lista normal de Python, si insertas algo al inicio la computadora tiene que recorrer todos los datos un lugar a la derecha. En nuestras pruebas con 100,000 elementos, Python se tardó **253.5 µs** y nuestra lista enlazada solo **3.9 µs**
- **Para recorrer o buscar:** Aquí gana la lista normal de Python porque como guarda todos los datos juntos en la memoria fisica, recorrerlos es mucho más fluido 
- **Para eliminar al final:** Aquí nuestra lista sufre ya que es simplemente enlazada para borrar el último nodo tenemos que buscar al penúltimo desde el principio (O(n)). Ahí Python le gana sin esfuerzo (0.5 µs frente a 4,642.3 µs de nosotros)

**Nuestra decisión:** Como las calles reales de Orizaba solo tienen entre 2 y 36 nodos, cualquiera de las dos estructuras es rapidisima en el uso normal. Decidimos usar nuestra **`ListaEnlazada`** como base porque cumple con conectar tramos físicamente y es muy eficiente insertando, solo se usaron arreglos de Python para cosas rápidas como entregar las listas finales de las intersecciones.

## 5. Cómo funciona la función recursiva

La función `longitud_recursiva` calcula la distancia sumando cada tramo paso a pasito llamándose a si misma.

- **El caso base:** Si ya llegamos a un nodo que no tiene `siguiente` (el final de la calle), la funcion ya no suma nada y regresa el total
- **El caso recursivo:** Calculamos la distancia entre el nodo actual y el que sigue con haversine y se la sumamos a un `acumulador`. Pasarle un acumulador nos garantizo que la suma de decimales se hiciera en el mismo orden que el ciclo normal, dando exactamente el mismo resultado
- **El límite de la memoria:** La recursividad abre muchos espacios en la memoria (la pila). Si una lista es muy larga Python marca error. Por eso el código revisa la longitud de la calle al inicio con `sys.getrecursionlimit()` y si ve que va a tronar, manda un `RecursionError` para que no colapse el programa

## 6. Pruebas de tiempo y análisis

Usamos un script llamado `medir.py` que tomo la calle real de 36 nodos y se invento listas gigantes de 1,000, 10,000 y 100,000 nodos. En cada tamaño repitió las operaciones 31 veces para sacar una **mediana** justa usando el reloj de la computadora

**Tiempos que obtuvimos (en microsegundos µs)** *(Nuestra ListaEnlazada / Lista de Python)*:

| Operación | 36 nodos | 1,000 nodos | 10,000 nodos | 100,000 nodos |
|---|---:|---:|---:|---:|
| Recorrido simple | 1.4 / 1.2 | 36.9 / 29.6 | 333.0 / 280.3 | 4,365.3 / 3,298.0 |
| Longitud (while) | 26.6 / 28.7 | 726.1 / 826.6 | 7,338.1 / 8,262.9 | 73,099.5 / 80,669.8 |
| Insertar inicio | 0.5 / 0.3 | 0.7 / 0.7 | 1.0 / 3.9 | 3.9 / 253.5 |
| Eliminar inicio | 0.3 / 0.2 | 0.5 / 0.4 | 1.4 / 2.1 | 3.2 / 25.0 |
| Insertar final | 0.5 / 0.2 | 0.8 / 0.4 | 1.1 / 0.5 | 4.5 / 187.6 |
| Eliminar final | 1.7 / 0.2 | 41.5 / 0.2 | 424.9 / 0.3 | 4,642.3 / 0.5 |

![Comparación de tiempos empíricos](../grafica_mediciones.png)

**Lo que notamos:**
Se comprobo que en nuestra lista, todas las funciones que tenían que recorrer nodos de uno por uno (como sumar la longitud o borrar en medio) se multiplicaban por 10 en tiempo cada vez que multiplicábamos por 10 los nodos (crecimiento lineal O(n)). En cambio operaciones como insertar al inicio se mantuvieron súper bajas (debajo de 4.5 µs) sin importar si eran 36 o 100,000 nodos, confirmando que son constantes O(1)

## 7. Las pruebas que hicimos

Le pedimos a la IA que nos generara un script llamado `pruebas.py` con 23 asserts para comprobar que todo funcionara bien. Y ya nos encargamos de correr el archivo en la consola, detectar en donde marcaba error el programa y pedirle las correcciones a la máquina hasta que pasaran todos los casos en limpio. Las pruebas checaban:
- Meter y borrar nodos en las orillas y en medio.
- Casos raros, como tratar de borrar algo en una lista vacía o de 1 solo nodo
- Correr 1,500 operaciones al azar al mismo tiempo en nuestra lista y en la de Python para comprobar que las dos terminaran con los mismos datos exactamente.
- Verificar el XML simulando una calle que va al revés (`oneway=-1`) y checando que el programa no pusiera cruces falsos

## 8. Límites de nuestro código

- Al ser una lista simplemente enlazada, borrar el último nodo siempre será O(n). Para hacerlo mas rápido tendríamos que usar una lista doblemente enlazada, pero gastaría más memoria guardando el puntero "anterior"

## 9. Cómo correr el proyecto

Solo usamos cosas que ya vienen instaladas en Python 3.10 o superior (excepto para la gráfica que requiere `matplotlib`) desde la terminal:

```bash
python main.py          # Carga el mapa, cuenta las calles y cruces
python pruebas.py       # Corre las 23 pruebas para ver que nada falle
python medir.py         # Mide los tiempos y hace el archivo .csv
python graficar.py      # Lee el .csv y dibuja la imagen
```

## 10. Uso de IA y trabajo en equipo

Como mencionamos en docs/bitacora.md usamos el modelo Claude para apoyarnos con el codigo porque la logica de los punteros se nos complicó desde el comienzo, asi que samos la inteligencia artificial para que nos diera la estructura del codigo, pero no centramos en entender como se conectaban las cosas, forzarlo a respetar las reglas del proyecto corriendo el programa una y otra vez y aplicar la logica a los archivos haversine.py e intersecciones.py

El docente nos comentó que la sugerencia es que con apoyo del LLM podamos saber adecuadamente que significa lo que se genera, de lo contrario podríamos vernos confundidos. Por eso tambien nos enfocamos en estudiar y entender el codigo que entregamos

Fuente de datos: © OpenStreetMap contributors, ODbL 1.0.