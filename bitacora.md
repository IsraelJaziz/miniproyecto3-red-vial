# Bitácora del Miniproyecto 3

Planificador de rutas sobre la red vial urbana · Zona Centro de Orizaba · Estructuras de Datos
Catedrático: Dr. Ulises Juárez Martínez · Entrega: 15 de octubre de 2026

Esta bitácora registra como nos organizamos para el proyecto, las decisiones que tomamos con el código y como utilizamos el LLM para apoyarnos con la programación, enfocandonos en entender y corregir lo que la IA generaba

## 1. Equipo

| Integrante | Usuario de GitHub |
|---|---|
| Díaz Bello Israel Jaziz | IsraelJaziz |
| Pérez Virgen Emiliano | Emi03LC |
| Miranda Chávez Gabriela | Gabriela-Mirandaa |

El equipo estaba originalmente conformado por cuatro integrantes pero el cuarto compañero no participó ni respondió a los mensajes asi que el 12 de octubre decidimos continuar el proyecto con solo tres integrantes

## 2. Distribución del trabajo

| Integrante | Qué hizo | Evidencia |
|---|---|---|
| Díaz Bello Israel Jaziz | Se encargo del código base (`lista_enlazada.py`, `main.py`). Le pidió a la IA la estructura inicial y se dedicó a revisar que los punteros funcionaran bien. También le pidió corregir los problemas con la recursión (usando `sys.getrecursionlimit()`) y armó la solución del Problema 3 pidiéndole a Claude usar un diccionario. | Commits de actualización de `lista_enlazada.py`, `secuencia_contigua.py` y `main.py`; sección 5 |
| Miranda Chávez Gabriela | Se encargo de leer el XML (`red_vial.py`) y de las pruebas (`pruebas.py`). Usó la IA para armar los filtros de las calles vehiculares, corrigió la lógica para voltear las calles de un sentido (`oneway=-1`) y le pidió a la IA que generara los casos de prueba, encargándose de correrlos en la consola y regresarle los errores a Claude para que los corrigiera. | Commits de `red_vial.py`, `pruebas.py` y `docs/`; sección 5 |
| Pérez Virgen Emiliano | Se encargo de los scripts para medir tiempos (`medir.py`) y hacer las graficas (`graficar.py`). Le pidió el código a la IA y revisó que el temporizador funcionara tambien corrió las pruebas finales en su laptop para generar el archivo CSV y subió el mapa original de OpenStreetMap. | Commits de `medir.py`, `graficar.py` y PNG; sección 5 |

## 3. Decisiones prácticas de diseño

| # | Fecha | Decisión | Por qué |
|---|---|---|---|
| 1 | 2026-10-10 | **Separar el código en varios archivos** | Al principio la IA nos generó todo en un solo archivo gigante y para no perdernos al leerlo, le pedimos que separara la estructura de datos en uno y el procesamiento del mapa en otro |
| 2 | 2026-10-10 | **Leer el archivo OSM en dos pasadas** | La IA tarto de leer el mapa completo de una vez, pero consumía mucha memoria asi que mejor le pedimos una opción mas ligera y nos implementó la lectura en dos pasos: primero guardar coordenadas y luego armar las calles. |
| 3 | 2026-10-11 | **Filtrar la red vial estrictamente por `highway`** | Como la rúbrica pedia calles vehiculares tuvimos que revisar que etiquetas traía el mapa de Orizaba y darle la instrucción exacta a Claude para que ignorara parques o edificios. |
| 4 | Código base | **Agregar el puntero `cola` a la lista** | La primera lista enlazada que nos dio la IA era muy lenta para insertar nodos al final mejor le preguntamos cómo optimizarla y nos sugirió agregar este puntero para hacerlo más rápido en tiempo O(1). |
| 5 | 2026-10-11 | **Usar `sys.getrecursionlimit()` en vez de forzar la memoria** | Para no modificar el límite de recursión de Python, le pedimos que mejor validara el límite con `sys.getrecursionlimit()` y lanzara un error controlado |
| 6 | 2026-10-11 | **Usar un diccionario para el Problema 3** | El primer código de la IA para buscar intersecciones usaba ciclos `for` que iban a tardar mucho. Le pedimos que lo hiciera más eficiente y nos cambió la lógica a un diccionario para que la búsqueda fuera en tiempo O(1) |
| 7 | 2026-10-11 | **Probar con listas inventadas de 100,000 nodos** | Al medir las calles reales (la más larga tenía 36 nodos), la gráfica casi no mostraba diferencias de tiempo. Decidimos pedirle a la IA que generara listas simuladas gigantes para poder ver bien el contraste en las mediciones. |
| 8 | 2026-10-13 | **Exportar los tiempos a un CSV antes de graficar** | El script original de la IA que medía y graficaba al mismo tiempo nos marcaba muchosisimos errores mejor decidimos pedirle que separara las tareas: un script saca el `.csv` y otro script solamente lo lee y dibuja la imagen |

## 4. Uso de LLM

**Modelo utilizado:** Claude  

Desde el comienzo el manejo de memoria y los punteros en Python se nos complicó bastante y nos bloqueamos. Decidimos usar Claude para que nos diera el código base y la sintaxis. Nuestro trabajo fue leer el código, probarlo, ver los errores que salían en la terminal y pedirle a la IA que los corrigiera hasta que todo cumpliera con la rubrica.

El docente nos comentó que la sugerencia es que con apoyo del LLM podamos saber adecuadamente qué significa lo que se genera, de lo contrario podríamos vernos confundidos

### Cómo trabajamos con la IA

- **Lectura del archivo (10 de octubre):** Le pedimos ayuda para leer el `.osm`. La IA nos dio códigos que leían todo de golpe pero investigamos y vimos que eso saturaba la memoria mejor le pedimos que lo cambiara a `ET.iterparse` 
- **Ajustes y correcciones (11 - 13 de octubre):** 
  - Corregimos la recursión porque los decimales variaban; le pedimos a la IA que metiera un acumulador (`acum + dist`).
  - Para las vías invertidas (`oneway=-1`), la IA quería crear todos los nodos y luego invertir la lista. Nos dimos cuenta de que era mejor invertir los números directo en Python con `refs.reverse()` antes de armar la lista
- **Hacer las pruebas:** Le pedimos a la IA que nos armara un script para comprobar que el código funcionara y nos generó un archivo con 23 casos usando `assert`. Nuestro trabajo aquí fue ejecutar el archivo, ver qué pruebas tronaban en la consola, copiar esos errores y pasárselos de vuelta a Claude para que ajustara el código principal hasta que todo pasó limpio

## 5. Entradas personales

Lo que aprendió y revisó cada integrante durante el proyecto:

### Díaz Bello Israel Jaziz

| Fecha | Qué hice | Qué entendí / qué dudas resolví |
|---|---|---|
| 2026-10-10 | Le pedí a Claude la primera versión de `lista_enlazada.py` y `main.py`. Revisé cómo funcionaban `cabeza` y `cola`. Realize algunas pruebas sueltas en un archivo `variantes.py`, que después eliminamos (13 de octubre) porque ya no hacía falta. | Me quedo claro por qué insertar al final con `cola` es O(1). Pero también vi que como nuestra lista es simple, si quieres eliminar el ultimo nodo a fuerza tienes que recorrer todo desde el inicio en O(n) porque no hay forma de ir hacia atrás. |
| 2026-10-13 | Corregí lo de los decimales pidiéndole a la IA que usara un acumulador en la recursión. Le pedi que metiera la validación del `RecursionError` y armé `secuencia_contigua.py` para comparar bien los tiempos | No entendía por qué el ciclo `while` y la recursión daban decimales un tanto diferentes. Aprendi que en punto flotante el orden importa: el acumulador fuerza a la recursión a sumar progresivamente igual que el ciclo |

### Miranda Chávez Gabriela

| Fecha | Qué hice | Qué entendí / qué dudas resolví |
|---|---|---|
| 2026-10-10 | Le pedí a la IA que nos armara la lectura del archivo. Vi que era mejor usar `iterparse` y cheque que se guardaran bien los nodos en el diccionario temporal. | Entendi mejor como viene estructurado OpenStreetMap. Las calles no traen latitud y longitud, solo traen un número (ID). Si no guardábamos las coordenadas primero, el programa iba a ser muy lento al buscar nodo por nodo. |
| 2026-10-12 | Revisé cómo la IA estaba manejando las calles que van al revés (`oneway=-1`). La opcion que usara `refs.reverse()` directo en la lista normal antes de crear nuestra lista enlazada era mejor asi que asi lo deje | Tiene sentido que al voltear los números de la lista antes de crear la calle nos ahorraramos mucha memoria en lugar de crear la calle mal y luego tener que desarmarla |
| 2026-10-14 | Le pedí a la IA que armara el script de `pruebas.py` y me dio 23 casos diferentes. Tuve que correr el código, leer los errores cuando algo no funcionaba en la consola y pedirle a Claude que lo corrigiera hasta que no marcara ningún error. | Al correr los asserts, me di cuenta de la importancia de probar los casos límite. Tambien al probar el Problema 3, vi que usar un diccionario para buscar intersecciones es inmediato (tiempo O(1)). Si hubieramos usado un `for` se hubiera tardado muchisimo. |

### Pérez Virgen Emiliano

| Fecha | Qué hice | Qué entendí / qué dudas resolví |
|---|---|---|
| 2026-10-12 | Descargué el mapa original `red_vial_orizaba_centro.osm` y lo abrí para ver como estaban escritas las etiquetas de `<node>` y `<way>`. | Abrir el XML me sirvió para entender qué era lo que le estábamos pidiendo a la IA que leyera y confirmar que no estuviera poniendo datos incorrectos |
| 2026-10-13 | Le pedi a la IA los scripts de `medir.py`. Me di cuenta de que el código no borraba la lista antes de volver a medir asi que se lo di a corregir, saque los tiempos reales con 100,000 nodos y revise la grafica. | Vi que la lista nativa de Python es muy rapida barriendo datos pero al querer insertar algo al mero inicio de 100,000 nodos, nuestra lista enlazada le gana por mucho porque solo tiene que mover un puntero |

## 6. Cómo se verificó el trabajo

| Verificación | Resultado obtenido |
|---|---|
| Ejecución de `python main.py` | Carga 8,741 nodos y 1,874 ways; filtra 355 vías vehiculares válidas, detecta 453 intersecciones y calcula la longitud de la vía 892777216 en `1634.1844456391464 m` (exactamente igual en iterativo y recursivo) |
| Ejecución de `python pruebas.py` | Pasan los 23 casos generados y corregidos (operaciones en inicio, medio y final, listas vacías, prueba de invertir, límite de recursión y filtrado de XML). |
| Ejecución de `medir.py` y `graficar.py` | Genera `resultados_mediciones.csv` sacando la mediana de 31 repeticiones en tamaños 36, 1,000, 10,000 y 100,000, y produce `grafica_mediciones.png`. |
| Archivos originales | `haversine.py`, `intersecciones.py` y `red_vial_orizaba_centro.osm` se mantienen sin ningun cambio |