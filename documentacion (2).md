# 🛒 Proyecto Aurelion

# Sprint 1

## 📌 Tema, problema y solución

**Tema:** Gestión de productos y análisis de ventas de un supermercado.  

El supermercado **“Aurelion”** registra la información de clientes, productos y ventas en diferentes archivos de Excel.  
Con el objetivo de organizar el stock y optimizar las ventas para las fechas navideñas, se busca centralizar y analizar los datos de forma más eficiente.

### 🧩 Problemas identificados
- Duplicidad de datos y dificultad para actualizarlos.
- Falta de control sobre el stock disponible.
- Limitaciones para realizar el análisis de ventas por fechas o temporadas (como por ejemplo, la época navideña).

Como consecuencia la administración enfrenta retrasos en la toma de decisiones, desabastecimiento o excesos de inventario y poca capacidad para planificar campañas de venta efectivas.

### 💡 Solución propuesta
Integrar los archivos de Excel existentes en un mismo entorno de trabajo (**VS Code**) y desarrollar un programa en **Python** que:
- Lea los datos desde los archivos: `clientes.xlsx`, `productos.xlsx`, `ventas.xlsx` y `detalle_ventas.xlsx`.  
- Permita realizar consultas automáticas sobre las ventas y productos.  
- Genere reportes simples, como el total de ventas y los productos más vendidos.  

---

## 📊 Dataset de referencia

### Fuente y definición
Los datos provienen de los registros internos del supermercado Aurelion. Se utilizan archivos Excel (.xlsx) como fuente de información principal para simular una base de datos relacional dentro del entorno Python.  

### Estructura, tipos y escala

| Tabla | Descripción | Campos principales | Relación |
|--------|--------------|--------------------|-----------|
| **clientes** | Contiene los datos de los clientes del supermercado. | `id_cliente`, `nombre`, `apellido`, `correo`, `telefono`, `direccion` | 1 a muchos con `ventas`. |
| **productos** | Registra los artículos disponibles en el supermercado. | `id_producto`, `nombre_producto`, `categoria`, `precio_unitario`, `stock_actual` | 1 a muchos con `detalle_ventas`. |
| **ventas** | Guarda la información general de cada venta realizada. | `id_venta`, `id_cliente`, `fecha_venta`, `total_venta` | 1 a muchos con `detalle_ventas`. |
| **detalle_ventas** | Desglosa los productos incluidos en cada venta. | `id_detalle`, `id_venta`, `id_producto`, `cantidad`, `subtotal` | Muchos a uno con `ventas` y `productos`. |

**Tipo de base de datos:** Relacional  
**Formato actual:** Archivos Excel (.xlsx)  
**Gestión:** Lectura mediante librerías `pandas` y `openpyxl`.  
**Escala:** Pequeña a mediana (decenas de clientes, cientos de productos y miles de ventas).  

---

## ⚙️ Información, pasos, pseudocódigo y diagrama

### 🔁 Flujo general del programa
1. Acceder a la carpeta del proyecto “Proyecto Aurelion”.  
2. Mostrar los archivos disponibles.  
3. Solicitar al usuario el nombre del archivo que desea abrir.  
4. Validar que el archivo exista en la lista.  
5. Si el archivo es `documentacion.md`, mostrar su contenido.  
6. Manejar errores de lectura, permisos o inexistencia del archivo.  
7. Finalizar el proceso con mensaje informativo.

### 💻 Pseudocódigo

```plaintext
INICIO
    ABRIR_CARPETA("Proyecto Aurelion")
    MOSTRAR_ARCHIVOS: ["clientes.xlsx", "productos.xlsx", "ventas.xlsx", "detalle_ventas.xlsx", "documentacion.md"]
    ESCRIBIR "Ingrese el nombre del archivo al que desea acceder:"
    LEER nombre_archivo

    SI nombre_archivo = "documentacion.md" ENTONCES
        LEER_ARCHIVO("documentacion.md")
        ESCRIBIR "Contenido de doc.md leído exitosamente"
    SINO
        ESCRIBIR "Fin del proceso"
    FINSI
FIN
```

### 🧭 Diagrama de flujo del programa

![Diagrama de flujo del Proyecto Aurelion](proyecto%20aurelion.drawio.png)

---

## 🤖 Sugerencias y mejoras aplicadas con Copilot

1. **Manejo de casos:** se incorporó la comparación *case-insensitive* al validar los nombres de archivos.  
2. **Validación de entrada:** se añadió verificación para comprobar si el archivo ingresado existe en la lista.  
3. **Manejo de excepciones:** ahora se manejan los errores `FileNotFoundError`, `PermissionError` y `Exception` general.  
4. **Mensajes descriptivos:** se mejoró la retroalimentación al usuario con mensajes informativos y claros.  
5. **Sugerencia de Copilot:** autocompletado de bloques de código, docstrings y validaciones condicionales.  
6. **Estructura final:** código más legible, organizado y modular, listo para futuras expansiones.

---

## 📈 Resultados esperados
El sistema permite acceder y validar archivos del proyecto, leer el contenido de `documentacion.md` y mejorar el manejo de errores en la ejecución.  
Su estructura modular permite integrarlo fácilmente con análisis posteriores mediante `pandas` para la generación de reportes o dashboards.

---
# Sprint 2

##  Integración de datos y preparación del entorno

Durante esta etapa se unificaron las distintas fuentes de información (Clientes, Productos, Ventas y Detalle de Ventas) en un único archivo maestro denominado BD_AURELION.xlsx.

El entorno de desarrollo empleado fue Visual Studio Code, utilizando Python 3.x como lenguaje principal junto con diversas librerías de análisis y visualización de datos. Estas herramientas permitieron manipular archivos, generar gráficos y gestionar el sistema de forma eficiente.

A partir de esta base consolidada se desarrollaron los scripts de limpieza, análisis y visualización que dieron origen al sistema de menú en consola (Demo 1).


## 🧹 Limpieza, análisis y visualización de datos

En esta fase se llevó a cabo el proceso de limpieza, análisis y visualización de la base principal BD_AURELION.xlsx, compuesta por las hojas Clientes, Detalle_Ventas, Productos, Ventas y Mapeo_Categorías.

El objetivo fue garantizar la integridad y coherencia de la información, eliminando duplicados, corrigiendo inconsistencias y depurando valores redundantes. De este modo se aseguró la calidad de los análisis posteriores y la confiabilidad del modelo de aprendizaje automático.

También se elaboraron estadísticas descriptivas básicas y gráficos representativos que permitieron examinar la distribución y el comportamiento de las variables más relevantes del conjunto de datos.

## 1. Importación de librerías

Se incorporaron las herramientas necesarias para manipular, limpiar, analizar y visualizar la información:

import pandas as pd
import matplotlib.pyplot as plt
import openpyxl
import seaborn as sns


pandas: manipulación y depuración de estructuras tipo DataFrame.

matplotlib.pyplot: creación de gráficos personalizados.

openpyxl: lectura y escritura de archivos Excel (.xlsx).

seaborn: generación de visualizaciones estadísticas claras y atractivas.

---

## 2. Carga de los datos

Se definió la ruta local donde se encuentra el archivo Excel principal:

```python
ruta_excel = r"C:\Users\alvar\Documents\IBM\Karina Alvarez_Proyecto Aurelion\BD_AURELION.xlsx"
```

Posteriormente, se cargaron las hojas correspondientes:

```python
df_cliente = pd.read_excel(ruta_excel, sheet_name="Clientes")
df_detalle = pd.read_excel(ruta_excel, sheet_name="Detalle_Ventas")
df_producto = pd.read_excel(ruta_excel, sheet_name="Productos")
df_ventas = pd.read_excel(ruta_excel, sheet_name="Ventas")
df_map = pd.read_excel(ruta_excel, sheet_name="Mapeo_Categorias")
```

Cada hoja se almacenó en un **DataFrame independiente** para trabajar la limpieza y el análisis de forma individual.

---

## 3. Limpieza de datos

### 3.1 Clientes

- Se verificaron y eliminaron filas duplicadas, garantizando registros únicos.  
- Se calculó la **moda de la columna “ciudad”**, identificando la ciudad con mayor número de clientes.  
- Se generó una **gráfica de torta (pie chart)** que muestra la **distribución de clientes por ciudad**.

---

### 3.2 Detalle_Ventas

- Se eliminaron filas duplicadas.  
- Se calcularon medidas de tendencia central de la columna **importe**:
  - Media (promedio)
  - Mediana (valor central)
  - Moda (valor más frecuente)
- Se eliminaron las columnas **nombre_producto** y **precio_unitario** por ser redundantes con la hoja de productos.  
- Se generó un **histograma con líneas de referencia** para visualizar la distribución de importes junto con su media, mediana y moda.

---

### 3.3 Productos

- Se eliminaron posibles duplicados y se calcularon las medidas de tendencia central de **precio_unitario** (media, mediana y moda).  
- Se realizó la **recategorización de productos**, tomando como base la hoja **Mapeo_Categorias** que contiene las columnas *palabra_clave*, *categoria_general* y *prioridad*.

El siguiente fragmento de código muestra el proceso:

```python
df_map['palabra_clave'] = df_map['palabra_clave'].str.lower().str.strip()
df_map = df_map.sort_values(by="prioridad")

def clasificar_producto(nombre_producto):
    if pd.isna(nombre_producto):
        return "Otros"
    nombre = str(nombre_producto).lower()
    for _, fila in df_map.iterrows():
        if fila['palabra_clave'] in nombre:
            return fila['categoria_general']
    return "Otros"

df_producto['categoria_general'] = df_producto['nombre_producto'].apply(clasificar_producto)
```

Con esta función, cada producto se clasifica automáticamente según su nombre, evitando inconsistencias y ampliando la posibilidad de incorporar nuevas categorías en el futuro.

Se generó un **boxplot** (diagrama de caja) para analizar la **distribución del precio unitario por categoría**, lo que permite identificar rangos de precios y posibles valores atípicos.

---

### 3.4 Ventas

- Se eliminaron duplicados y columnas redundantes como *nombre_cliente* y *email*.  
- Se calculó la **moda de la columna “medio_pago”**, identificando el método de pago más utilizado.  
- Se generó un **gráfico de barras** con la frecuencia de los distintos medios de pago.

---

## 4. Exportación de los datos limpios

Finalmente, los DataFrames actualizados se exportaron a un nuevo archivo Excel llamado **BD_AURELION_LIMPIO.xlsx**, con las siguientes hojas:

- *Clientes_Limpio*  
- *Detalle_Ventas_Limpio*  
- *Productos_Limpio*  
- *Ventas_Limpio*  
- *Mapeo_Categorias*  

```python
ruta_salida = r"C:\Users\alvar\Documents\IBM\Karina Alvarez_Proyecto Aurelion\BD_AURELION_LIMPIO.xlsx"
```

```python
with pd.ExcelWriter(ruta_salida, engine='openpyxl') as writer:
    df_cliente.to_excel(writer, sheet_name='Clientes_Limpio', index=False)
    df_detalle.to_excel(writer, sheet_name='Detalle_Ventas_Limpio', index=False)
    df_producto.to_excel(writer, sheet_name='Productos_Limpio', index=False)
    df_ventas.to_excel(writer, sheet_name='Ventas_Limpio', index=False)
    df_map.to_excel(writer, sheet_name='Mapeo_Categorias', index=False)
```

De esta forma, se conservaron las versiones limpias y analizadas de todas las hojas en un único archivo.

---

## 5. Resultados generales

| Hoja de Excel | Duplicados | Columnas Eliminadas | Observaciones principales |
|----------------|-------------|----------------------|----------------------------|
| **Clientes** | 0 | Ninguna | Se obtuvo la ciudad más frecuente entre los clientes. |
| **Detalle_Ventas** | 0 | *nombre_producto*, *precio_unitario* | Se calcularon media, mediana y moda de los importes. |
| **Productos** | 0 | Ninguna | Se realizó la recategorización por palabra clave. |
| **Ventas** | 0 | *nombre_cliente*, *email* | El medio de pago más usado fue el **efectivo**. |

Durante esta fase no se detectaron valores atípicos significativos; sin embargo, estos se evaluarán nuevamente durante el análisis estadístico avanzado del modelo.

---

## 🧭 MENÚ CONSOLA – PROYECTO AURELION (DEMO 1)

Luego de implementar y validar los procesos de limpieza y análisis, se desarrolló una interfaz de menú en consola que permite ejecutar cada módulo del Proyecto Aurelion de forma sencilla y ordenada. Este módulo facilita la interacción del usuario con los procesos de limpieza, análisis y exportación de datos, ofreciendo una manera estructurada, intuitiva y eficiente de acceder a las principales funciones del sistema desde una única interfaz.


## ⚙️ FUNCIONALIDAD GENERAL

El menú principal presenta siete opciones numeradas, que el usuario puede seleccionar para ejecutar distintas operaciones sobre las bases de datos del proyecto.

### Opciones disponibles:

1. **CLIENTE – Limpieza y análisis**  
   Ejecuta el proceso de depuración, validación y análisis exploratorio de la base de datos de clientes.  
   Incluye la visualización de gráficos y métricas descriptivas.

2. **PRODUCTOS – Limpieza y análisis**  
   Realiza la limpieza y el análisis de la base de datos de productos, incluyendo la integración con el mapa de categorías (`df_map`) y la generación de gráficos.

3. **VENTAS – Limpieza y análisis**  
   Procesa la base de datos de ventas, detectando valores nulos, inconsistencias y tendencias de comportamiento en las transacciones.

4. **DETALLE DE VENTA – Limpieza y análisis**  
   Limpia y analiza los registros de detalle de venta, identificando productos más vendidos, totales por categoría y otros indicadores.

5. **Abrir documentación**  
   Abre el archivo `documentacion_demo1_con_diagrama1.md` alojado en GitHub, donde se detallan los procesos, diagramas y estructura general del proyecto.  
   Enlace directo:
   [Ver documentación en GitHub](https://github.com/luis0221/Proyecto-aurelion/blob/387b5910d4853f7c744af856ef37570d9343e048/documentacion_demo1_con_diagrama1.md)

6. **Exportar BD limpia**  
   Ejecuta el proceso completo de limpieza sobre todas las bases de datos y exporta los resultados en un archivo unificado, listo para su uso o integración posterior.

7. **Salir**  
   Finaliza la ejecución del programa.

---

## 🧩 ESTRUCTURA DEL CÓDIGO

### 1. `mostrar_menu()`
Muestra el menú principal en la consola, con todas las opciones disponibles para el usuario.

### 2. `abrir_documentacion()`
Abre en el navegador el archivo de documentación principal del proyecto alojado en GitHub.  
Incluye manejo de errores en caso de que la conexión falle.

### 3. `main()`
Función principal del programa.  
- Carga las bases de datos utilizando la función `cargar_datos()`.  
- Muestra el menú principal.  
- Ejecuta el bloque correspondiente según la opción seleccionada por el usuario.  
- Controla errores de entrada y permite salir de forma segura.  

El flujo principal se controla mediante un bucle `while True`, que mantiene activo el programa hasta que el usuario elige la opción **7 (Salir)**.

---

## 🧱 DEPENDENCIAS Y FUNCIONES RELACIONADAS

El menú utiliza las siguientes funciones auxiliares, definidas en otros módulos del proyecto:

- `cargar_datos()`  
  Carga las bases de datos originales en DataFrames de pandas.

- `limpiar_analizar_clientes(df_cliente, mostrar_graficos=True)`
- `limpiar_analizar_productos(df_producto, df_map, mostrar_graficos=True)`
- `limpiar_analizar_ventas(df_ventas, mostrar_graficos=True)`
- `limpiar_analizar_detalle(df_detalle, mostrar_graficos=True)`  
  Aplican los procesos de limpieza, análisis y visualización correspondientes a cada base de datos.

- `exportar_bd_limpia(df_cliente, df_detalle, df_producto, df_ventas, df_map)`  
  Genera y exporta una versión consolidada y depurada de la base de datos.

---

## 📊 ANÁLISIS ESTADÍSTICO Y VISUALIZACIÓN DE RESULTADOS  

En esta etapa del proyecto se realizó el análisis estadístico y la visualización de resultados utilizando los datos ya depurados de las hojas **Clientes**, **Detalle_Ventas**, **Productos** y **Ventas** del archivo **BD_AURELION.xlsx**.  
El objetivo fue describir las características principales de los datos mediante medidas de tendencia central y representaciones gráficas que faciliten su interpretación y permitan obtener conclusiones orientadas a la toma de decisiones.

---

## 1️⃣ Identificación del tipo de distribución de variables  

### 🧭 Gráfico de Clientes  
El gráfico de torta muestra la proporción de clientes por ciudad, evidenciando que **Río Cuarto concentra la mayor cantidad**, seguida por **Alta Gracia**, lo que refleja una fuerte presencia comercial en el interior provincial. Esta información es clave para optimizar la planificación logística y orientar las estrategias comerciales hacia las zonas más representativas.  

Desde el punto de vista **logístico**, permite optimizar rutas de entrega, planificar inventarios y evaluar la conveniencia de nuevos centros de distribución. En **marketing y ventas**, facilita la segmentación de campañas, la detección de mercados potenciales (como Córdoba y Mendiolaza) y la adaptación de promociones según la ubicación.  
A nivel **administrativo y financiero**, mejora la organización de recursos y el control presupuestario por región, mientras que en **atención al cliente** ayuda a distribuir mejor el personal y fortalecer los canales en zonas de mayor demanda.  

---

### 💰 Gráfico de Productos (Boxplot)  
El boxplot refleja la **distribución de precios** de las nueve categorías principales de productos. Las categorías **Snacks/Panadería** y **Alimento** presentan una mayor dispersión, lo que indica variedad de precios, mientras que **Bebidas** y **Legumbres** concentran los productos de mayor costo.  

El rango general de precios va de **menos de $1000 a casi $5000**, con diferencias notables entre categorías. En **Otros** y **Legumbres**, la mediana está centrada, mostrando una distribución simétrica. En **Limpieza**, la mediana se ubica en la parte inferior y aparece un punto aislado, indicativo de un valor atípico. La categoría **Higiene** también presenta un outlier.  

Este análisis permite **entender la estructura de precios**, ajustar estrategias de stock y evaluar políticas de precios equilibradas entre categorías, además de detectar posibles errores de carga o productos fuera de rango.  

---

### 📈 Histograma de Ventas  
El histograma de importes muestra que la mayoría de las observaciones se concentra entre **$2000 y $7000**, donde las barras alcanzan las frecuencias más altas (entre 50 y 60 registros).  
A medida que el importe aumenta, la frecuencia disminuye, evidenciando una **distribución asimétrica positiva (sesgada a la derecha)**.  

La **moda** (línea amarilla) se encuentra en los valores bajos, la **mediana** (verde) un poco más a la derecha y la **media** (roja) aún más desplazada, confirmando la presencia de valores altos que elevan el promedio general.  
Esto sugiere que la mayoría de las ventas corresponden a montos bajos o medios, con pocas operaciones de alto importe que impactan en el promedio total.  

---

### 💳 Gráfico de Barras – Medios de Pago  
El gráfico de barras muestra la **distribución del uso de los distintos medios de pago**, destacando que el **efectivo** es el más utilizado, seguido por **QR**, mientras que **transferencia** y **tarjeta** tienen una menor participación.  

Este patrón refleja una **preferencia marcada por los medios tradicionales** y una **adopción más lenta de opciones digitales**.  
Desde la gestión administrativa, esto implica un mayor manejo de dinero en efectivo, lo que requiere **controles más estrictos de caja y conciliación**.  

Desde **marketing y ventas**, se observa una oportunidad para **incentivar el uso de medios electrónicos** mediante beneficios o campañas promocionales, lo que podría agilizar los procesos de cobro, mejorar la experiencia del cliente y aumentar las ventas al ofrecer más opciones de pago.  

---

## 2️⃣ Detección de outliers  

En la categoría **Limpieza** del gráfico boxplot se detectó un valor atípico por encima del rango habitual, y otro similar en **Higiene**. Estos valores pueden deberse a productos especiales o errores de carga, por lo que conviene **verificarlos** antes de realizar análisis predictivos o de rentabilidad.  

En el histograma, la diferencia entre **media, mediana y moda** también indica **valores atípicos altos** que influyen en la media general.  
Estos casos requieren atención, ya que pueden distorsionar la percepción de las ventas promedio y afectar la interpretación de resultados.  

Identificar y tratar los outliers garantiza una **mayor fiabilidad del análisis** y permite establecer umbrales realistas para decisiones de precios, rentabilidad y proyecciones futuras.  

---

## 3️⃣ Análisis de correlaciones entre variables principales  

La matriz de correlación evidencia una **relación positiva moderada (r = 0.60)** entre la cantidad de productos vendidos y el importe total.  
Esto significa que, en general, al aumentar la cantidad vendida también crece el valor total de la venta, aunque no siempre de manera proporcional, debido a factores como el precio unitario o la categoría del producto.  

Esta correlación sugiere que las estrategias comerciales deberían enfocarse no solo en aumentar el volumen de ventas, sino también en **potenciar los productos de mayor valor o margen**, optimizando así los ingresos sin necesidad de incrementar significativamente la cantidad de unidades vendidas.  

---

## 🧾 Conclusión general  

El análisis realizado permite comprender en profundidad el comportamiento de **ventas, productos y clientes** de la tienda **Aurelion**, así como su distribución geográfica y económica.  

En conjunto, se observa que las ventas se concentran en **montos bajos a medios**, existe **variabilidad de precios significativa entre categorías**, predomina el **uso de medios de pago tradicionales** y se identifica una **fuerte concentración de clientes en zonas clave**.  

Estos hallazgos orientan la toma de decisiones estratégicas en **administración, marketing, finanzas y logística**, fortaleciendo la planificación de inventarios, la segmentación de campañas, la optimización de rutas y la gestión eficiente de recursos.  

✨ En resumen, el análisis confirma que la **base de datos se encuentra limpia, coherente y lista para su uso en etapas posteriores de análisis y modelado**, constituyendo una base sólida para **decisiones informadas y sostenibles** que impulsen la rentabilidad y eficiencia del negocio.  

---


# Sprint 3

## Modelos de Regresión, Clasificación y Métricas de Inventario

## 1. Objetivo

 El objetivo es predecir la cantidad de unidades vendidas (demanda) mediante un modelo de regresión, con el propósito de estimar el stock óptimo que deberían tener los productos. A partir de la predicción de la variable cantidad, se busca anticipar rupturas de stock, identificar productos críticos y apoyar la planificación del inventario. Además, se generan clasificaciones derivadas del dataset y visualizaciones operativas para la toma de decisiones.

---

## 2. Dataset y Construcción del Modelo

 El script utiliza un archivo Excel con tres hojas principales:

- Productos

- Detalle_Ventas

- Dataset_Mensual

 Se realiza la unificación de datos mediante merge, agregando variables financieras y de stock al dataset mensual. Luego se eliminan valores nulos y se transforma el campo porcentaje_margen de cadena de texto a número. Esto permite consolidar un dataset limpio y listo para modelado.

---

## 3. Definición del Problema de ML

 ### Tipo de problema: Regresión supervisada.

 ### Objetivo principal: Predecir la cantidad vendida por producto, año y mes.

 Conocer la demanda futura permite calcular el stock óptimo y detectar riesgos de desabastecimiento.

---

## 4. Entradas (X) y Salida (y)

### Variable objetivo (y)
 - cantidad

### Variables de entrada (X)
 anio, mes, categoria_general,
 precio_unitario, costo_producto,
 margen_ganancia, porcentaje_margen,
 stock_actual, stock_minimo

Separación por tipo

Numéricas: anio, mes, precio_unitario, costo_producto, margen_ganancia, porcentaje_margen, stock_actual, stock_minimo

Categóricas: categoria_general

---

## 5. Modelo de ML Implementado

### Algoritmo elegido: Gradient Boosting Regressor

### Justificación: 

- Maneja relaciones no lineales entre variables.

- Se ajusta bien a datos heterogéneos como precios, stocks y márgenes.

- Es robusto ante variaciones entre productos.

- Minimiza el sobreajuste mediante parámetros como max_depth, learning_rate y subsample.

- Generalmente supera a los modelos lineales en series con comportamiento irregular, como la demanda de productos.

---

## 6. Preprocesamiento Aplicado

 ### Se utiliza un ColumnTransformer dentro de un Pipeline:

 - StandardScaler() para variables numéricas

 - OneHotEncoder(handle_unknown="ignore") para la categoría

 - El Pipeline garantiza preprocesamiento consistente tanto en entrenamiento como en predicción.

---

## 7. División Train/Test y Entrenamiento

### División 80% entrenamiento / 20% test

 Semilla fija (random_state=42) para mantener reproducibilidad

 Entrenamiento con: modelo_reg.fit(X_train, y_train)


 Predicciones con:  y_pred = modelo_reg.predict(X_test)

---

## 8. Métricas de Evaluación

 El modelo imprime en consola las siguientes métricas:

 - MAE: error absoluto promedio (qué tan lejos estamos en unidades reales)

 - RMSE: penaliza más los errores grandes

 - R²: porcentaje de variabilidad explicada por el modelo

 Estas métricas permiten medir estabilidad y capacidad predictiva.

---

## 9. Clasificación (Reglas Basadas en Datos)

 Además del modelo de regresión, se genera una clasificación no supervisada basada en reglas:

 ### Clasificación por demanda (nivel_ventas)

 - TOP: ventas ≥ percentil 80

 - MEDIO: entre percentil 30 y 80

 - BAJO: ventas ≤ percentil 30

 ### Clasificación por riesgo de stock

 Basado en el stock actual versus el mínimo:

 - ALTO_RIESGO

 - MEDIO_RIESGO

 - SIN_RIESGO

 Estas categorías alimentan los gráficos de criticidad creados más adelante.

---

## 10. Predicción Mensual Especial – Diciembre

 Se construye un segundo modelo de regresión para predecir el valor total de ventas mensuales del último período disponible, especialmente diciembre.

### Variables utilizadas:

 mes_num (índice temporal)

 rolling_3 (media móvil 3 meses)

 precio_promedio

 costo_promedio

 El modelo predice automáticamente la cantidad estimada para diciembre y la muestra en consola.

---

## 11. Gráficos Generados

### 11.1 Top 20 Productos con Mayor Demanda Real

- Se agrupan todas las ventas por producto.  
- Se obtienen los 20 de mayor cantidad vendida.  
- Se grafica un ranking comparativo.  

El gráfico incluye una anotación automática destacando: ➡️ Producto con mayor demanda real.

---

### 11.2 Predicción de Ventas de Diciembre

A partir del dataset mensual se calcula:

- cantidad_total  
- precio_promedio  
- costo_promedio  
- fecha del mes  
- número de mes (`mes_num`)  
- media móvil de 3 meses (`rolling_3`)  

### Modelo utilizado

**GradientBoostingRegressor**, con:

- `n_estimators = 300`  
- `learning_rate = 0.05`  
- `max_depth = 4`  
- `subsample = 0.9`

Genera: ➡️ Predicción de ventas para diciembre del último año disponible.  
El valor aparece tanto en consola como en el gráfico.

---

### 11.3 Riesgo de Desabastecimiento

Se calcula el ratio:

```
ratio = stock_actual / stock_minimo
```

Se seleccionan los productos con ratio ≤ 1.5.  
Del grupo, se muestran los 20 más críticos.

El gráfico compara:

- Stock mínimo  
- Stock actual  

Y destaca: ➡️ Producto con menor stock relativo frente al mínimo.

---

### 11.4 Productos TOP Críticos (Alta Demanda + Bajo Stock)

Se cruzan ambas condiciones:

1. Producto clasificado como **TOP**.  
2. Stock crítico (`stock_actual < stock_minimo × 1.2`).  

Se muestran los 20 más relevantes.

Si existe uno claramente crítico, se agrega una anotación indicando: ➡️ Producto TOP más crítico (demanda total + stock actual).

---

## 12. Conclusión General 

 El modelo integra predicción de demanda, análisis de inventario y clasificación operativa para facilitar decisiones estratégicas relacionadas con:

 * planificación de compras

 * reposición de stock

 * control de inventario

 * prevención de quiebres

 * priorización de productos críticos

 El resultado final permite anticipar variaciones de demanda y ajustar los niveles de inventario para lograr mayor eficiencia y continuidad operativa.



 ---

# Sprint 4 

## Documentación Power BI  
### Análisis de Desempeño Comercial y Control de Stock

En esta sprint se desarrolló un dashboard integral en Power BI orientado al análisis del desempeño comercial, la identificación de productos con mayor demanda y el control de stock crítico. El trabajo abarcó todo el flujo del proyecto: desde la importación y preparación de datos hasta la construcción de KPIs y visualizaciones con enfoque ejecutivo.

---

## Importación de la base de datos

La base de datos utilizada en este proyecto se denomina **BD_AURELION_ENTRENABLE_FINAL.xlsx**.  
Contiene información histórica de la tienda Aurelion desde el año 2023 hasta noviembre de 2025, con más de 54.000 registros relacionados con ventas, productos, clientes y stock.

Este archivo fue importado a Power BI como punto de partida del proceso de modelado y análisis.

tablas principales:

- Ventas  
- Detalle_Ventas  
- Productos  
- Clientes  
- Dataset_Mensual  
- Mapeo_Categorias  

---

## 2. Limpieza y preparación de datos (Power Query)

En Power Query se realizaron tareas de limpieza y normalización, entre ellas:

- Corrección de tipos de datos (fechas, numéricos y texto).
- Eliminación de columnas innecesarias para el análisis.
- Revisión de valores nulos y duplicados.
- Estandarización de nombres de campos para facilitar el modelado.
- Validación de claves entre tablas (IDs de producto, fechas, etc.).

Estas acciones permitieron garantizar la calidad de los datos y un correcto funcionamiento del modelo relacional.

---

## 3 Creación de la tabla Calendario

Se creó una tabla calendario dinámica mediante DAX, tomando como referencia el rango de fechas existente en la tabla Ventas. Esto permite que el modelo se actualice automáticamente si se incorporan nuevos datos.

Esta tabla permite realizar análisis temporales por año, mes, trimestre y día, y fue utilizada para la creación de jerarquías de fechas y cálculos comparativos entre períodos.

```DAX
Calendario =
VAR FechaMin = MIN ( Ventas[Fecha] )
VAR FechaMax = MAX ( Ventas[Fecha] )
RETURN
ADDCOLUMNS (
    CALENDAR ( FechaMin, FechaMax ),
    "Año", YEAR ( [Date] ),
    "Mes", FORMAT ( [Date], "MMMM" ),
    "Mes Nº", MONTH ( [Date] ),
    "Año-Mes", FORMAT ( [Date], "YYYY-MM" ),
    "Trimestre", "T" & FORMAT ( [Date], "Q" ),
    "Día", DAY ( [Date] ),
    "Día Semana", FORMAT ( [Date], "dddd" )
)
```

---

## 4. Creación de relaciones entre tablas (Modelo de datos)


El modelo de datos fue diseñado siguiendo un esquema de tipo **estrella**, con el objetivo de optimizar el rendimiento del dashboard y garantizar la correcta interpretación de los indicadores.

### Tabla DIM Productos
- **Productos[Producto_ID]** (lado 1)  
- **Detalle_Ventas[Producto_ID]** (lado *)

Esta relación permite calcular métricas clave como ventas por producto, rotación de stock e identificación de productos críticos.

---

### Tabla DETALLE_VENTAS (tabla de hechos)

La tabla **Detalle_Ventas** actúa como la tabla fact principal del modelo, ya que contiene el detalle de cada producto vendido.

Relaciones:
- **Detalle_Ventas[Producto_ID] → Productos[Producto_ID]**
- **Detalle_Ventas[Venta_ID] → Ventas[Venta_ID]**

Esta tabla se ubica en el centro del modelo y concentra las métricas de cantidad e importe.

---

### Tabla VENTAS

La tabla **Ventas** representa el encabezado de cada transacción.

Relaciones:
- **Ventas[Venta_ID]** (1) → **Detalle_Ventas[Venta_ID]** (*)
- **Ventas[Cliente_ID]** (1) → **Clientes[Cliente_ID]** (*)

Esto permite analizar las ventas tanto a nivel de detalle como por cliente.

---

### Tabla CLIENTES

- **Clientes[Cliente_ID]** (lado 1)  
- **Ventas[Cliente_ID]** (lado *)

Esta relación permite segmentar las ventas por características del cliente, como zona o tipo de cliente.

---

### Tabla CALENDARIO

La tabla calendario se relaciona con la fecha de la venta:

- **Calendario[Date]** (lado 1)  
- **Ventas[Fecha]** (lado *)

Gracias a esta relación es posible:
- Analizar ventas por año, mes, día y trimestre.
- Detectar picos de venta y estacionalidades.
- Comparar períodos.
- Apoyar decisiones sobre stock óptimo según la demanda histórica.

---

### Tablas sin relación directa

- **Mapeo_Categorías**: no se relaciona con el modelo, ya que se utiliza únicamente como tabla auxiliar para la limpieza y normalización de categorías.
- **Dataset_Mensual**: no se relaciona al modelo principal, dado que es una tabla agregada y solo sería necesaria para análisis comparativos específicos.

Estas tablas se mantienen ocultas para no interferir con el modelo analítico.

---
### Resumen visual del modelo de datos

DIM Calendario (1)  
↓  
VENTAS (1) ─── Clientes (1)  
↓  
DETALLE_VENTAS (*)  
↑  
DIM Productos (1)  

Mapeo_Categorías → Oculta, sin relación  
Dataset_Mensual → Opcional, sin relación

---


## 5. Creación de la tabla de Medidas

Se creó una tabla específica denominada **Medidas**, organizada en carpetas para mejorar la mantenibilidad del modelo.

### 📁 Carpeta Ventas
```DAX
Ventas Totales =
SUM ( Ventas[total_venta] )

Unidades Vendidas =
SUM ( Detalle_Ventas[cantidad] )

Ventas Dic 2023 =
CALCULATE (
    [Ventas Totales],
    Calendario[Año] = 2023,
    Calendario[Mes Nº] = 12
)

Ventas Dic 2024 =
CALCULATE (
    [Ventas Totales],
    Calendario[Año] = 2024,
    Calendario[Mes Nº] = 12
)

Variacion % Dic =
DIVIDE (
    [Ventas Dic 2024] - [Ventas Dic 2023],
    [Ventas Dic 2023]
)

Meta Ventas Dic 2025 =
[Ventas Dic 2024] * ( 1 + [Variacion % Dic] )

Unidades Vendidas Dic 2025 =
CALCULATE (
    [Unidades Vendidas],
    Calendario[Año] = 2025,
    Calendario[Mes Nº] = 12
)
```
### 📁 Carpeta Stock
```DAX
Stock Actual =
SUM ( Productos[stock_actual] )

Stock Minimo =
SUM ( Productos[stock_minimo] )

Stock Critico? =
IF (
    [Stock Actual] <= [Stock Minimo],
    "CRITICO",
    "OK"
)

Cantidad Productos Críticos =
VAR _can =
    CALCULATE (
        COUNTROWS ( Productos ),
        Productos[stock_actual] <= Productos[stock_minimo]
    )
RETURN
    IF ( ISBLANK ( _can ), 0, _can )
```

### 📁 Carpeta Producto
```DAX
Ingreso por Producto =
CALCULATE (
    SUM ( Detalle_Ventas[importe] ),
    ALLEXCEPT ( Productos, Productos[nombre_producto] )
)

Producto Top 1 =
VAR TablaTop =
    TOPN (
        1,
        SUMMARIZE (
            Productos,
            Productos[nombre_producto],
            "Unidades", [Unidades Vendidas]
        ),
        [Unidades],
        DESC
    )
RETURN
    MAXX ( TablaTop, Productos[nombre_producto] )

Producto Top Demanda =
VAR TopProd =
    TOPN (
        1,
        ALL ( Productos[nombre_producto] ),
        [Unidades Vendidas Dic 2025],
        DESC
    )
RETURN
    CONCATENATEX ( TopProd, Productos[nombre_producto], ", " )

Ranking Demanda Producto =
RANKX (
    ALL ( Productos[nombre_producto] ),
    [Unidades Vendidas Dic 2025],
    ,
    DESC
)

Unidades Producto Top 1 =
VAR TablaTop =
    TOPN (
        1,
        SUMMARIZE (
            Productos,
            Productos[nombre_producto],
            "Unidades", [Unidades Vendidas]
        ),
        [Unidades],
        DESC
    )
RETURN
    MAXX ( TablaTop, [Unidades] )
```
---

## 6. Columna calculada en la tabla Productos

Se creó una columna calculada para clasificar el estado del stock por producto:

Esta columna se utiliza para filtros, segmentadores y análisis visual del riesgo de quiebre de stock.

```DAX
Estado Stock =
IF (
    Productos[stock_actual] <= Productos[stock_minimo],
    "CRITICO",
    "OK"
)
```
---

## KPIs y páginas del dashboard

El **Dashboard del Sprint 4** fue desarrollado para analizar el desempeño comercial y el riesgo de inventario de la tienda **Aurelion**, con foco en los años **2023 y 2024**, incorporando además una proyección para diciembre de 2025.

El punto de partida fue un reto significativo: la empresa contaba con una base de datos extensa, con más de **54.000 registros** correspondientes al período 2023–noviembre 2025. Sin embargo, esta información presentaba diversos problemas que limitaban la toma de decisiones estratégicas.

Entre las principales dificultades se identificaron:
- Duplicidad de registros.
- Dificultad para actualizar la información.
- Falta de control claro sobre ventas y niveles de stock.

Estas limitaciones impedían realizar análisis temporales confiables, como comparaciones mes a mes o el estudio de períodos clave del negocio, por ejemplo la **temporada navideña**.

Como consecuencia, resultaba complejo identificar:
- Productos con mayor rotación.
- Productos con riesgo de desabastecimiento.
- Productos con baja salida y sobrestock.

En este contexto, no existía una base sólida para optimizar el inventario ni para diseñar estrategias comerciales efectivas.

---

### Preguntas clave de negocio

A partir de esta situación, el dashboard fue diseñado para responder las siguientes preguntas:

1. ¿Cómo se comportaron las ventas en diciembre de 2023 versus diciembre de 2024?
2. ¿Se observa un crecimiento sostenido en las ventas?
3. ¿Qué productos presentan mayor demanda en cada período?
4. ¿Cuántos productos se encuentran en stock crítico, por debajo del nivel mínimo?
5. En términos generales, ¿cuál es el estado del inventario de la tienda?

Cada página del dashboard responde a una de estas preguntas mediante KPIs específicos y visualizaciones orientadas a la toma de decisiones.

---

### Overview – Desempeño Comercial y Stock

La página **Overview** presenta una visión general del negocio, integrando indicadores clave de ventas y stock. Su objetivo es brindar una lectura rápida del estado de la tienda, destacando:

- Ventas totales.
- Variación porcentual interanual.
- Cantidad de productos en stock crítico.
- Ranking de productos más vendidos.

Esta vista funciona como punto de partida para el análisis detallado de los KPIs.

---

### KPI 1 – Comparación de Ventas (Diciembre)

Este KPI analiza la comparación interanual de las ventas de diciembre 2023 y diciembre 2024, permitiendo evaluar el crecimiento del negocio. Incluye:

- Ventas de diciembre 2023.
- Ventas de diciembre 2024.
- Variación porcentual.
- Proyección de ventas para diciembre 2025.

La información obtenida sirve como base para establecer objetivos futuros y evaluar el desempeño comercial.

---

### KPI 2 – Producto con Mayor Demanda

Este KPI identifica el producto con mayor nivel de demanda, considerando:

- Producto más vendido.
- Cantidad de unidades vendidas.
- Ranking de productos por unidades.
- Detalle de ingresos por producto.

Este análisis aporta información clave para decisiones comerciales y de reposición de stock.

---

### KPI 3 – Control de Stock Crítico

El KPI de stock crítico permite detectar productos con riesgo de quiebre, facilitando acciones preventivas. Se analizan:

- Cantidad de productos en estado crítico.
- Comparación entre stock actual y stock mínimo.
- Estado del stock por producto.

Esta página es fundamental para la gestión eficiente del inventario.

---

## Conclusiones

El desarrollo de esta sprint permitió construir un dashboard robusto y alineado a criterios de negocio, integrando de manera efectiva el análisis comercial y el control de inventario. La correcta modelación de los datos, el uso de medidas DAX y la aplicación de una narrativa visual clara facilitan la interpretación de la información y respaldan la toma de decisiones basadas en datos.

El dashboard permite visualizar y comprender el comportamiento general de la tienda, facilitando el seguimiento del desempeño comercial y la detección temprana de situaciones críticas.

En particular, las ventas de diciembre de 2024 presentan un crecimiento aproximado del **37%** respecto a diciembre de 2023, equivalente a unos **$12.000.000**, lo que habilita la proyección de ventas para diciembre de 2025 iguales o superiores a **$57.000.000**, consolidando una tendencia de crecimiento sostenido.

En relación con el inventario, el análisis evidencia que la mayoría de los productos se encuentra en niveles óptimos de stock. No obstante, se identifica **un producto en estado crítico**, lo que permite anticipar acciones de reposición y prevenir quiebres de stock.

En conjunto, este dashboard aporta valor real al negocio, ya que permite identificar oportunidades de crecimiento, optimizar la gestión del stock y mejorar la planificación comercial de manera preventiva y estratégica.





---




📌 Nota sobre las bases de datos utilizadas:

- **BD_AURELION.xlsx**: base original consolidada a partir de los archivos fuente.
- **BD_AURELION_LIMPIO.xlsx**: versión depurada y normalizada utilizada para análisis exploratorio y modelado.
- **BD_AURELION_ENTRENABLE_FINAL.xlsx**: versión final utilizada en Power BI para la construcción del modelo y el dashboard.





👨‍💻 **Autor**  
**EQUIPO 1**  
Proyecto académico desarrollado en colaboración con **IBM SkillsBuild** y **Guayerd**.

