# 🛒 Proyecto Aurelion

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
# 🧭 MENÚ CONSOLA – PROYECTO AURELION (DEMO 1)

Luego de implementar y validar los procesos de limpieza y análisis, se desarrolló una interfaz de menú en consola que permite ejecutar cada módulo del Proyecto Aurelion de forma sencilla y ordenada. Este módulo facilita la interacción del usuario con los procesos de limpieza, análisis y exportación de datos, ofreciendo una manera estructurada, intuitiva y eficiente de acceder a las principales funciones del sistema desde una única interfaz.
---

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


## ANÁLISIS ESTADÍSTICO Y VISUALIZACIÓN DE RESULTADOS
---

En esta parte del proyecto se realizó el **análisis estadístico y la visualización de resultados** utilizando los datos ya limpios de las hojas *Clientes*, *Detalle_Ventas*, *Productos* y *Ventas* del archivo **BD_AURELION.xlsx**.  
El propósito fue describir las características principales de los datos mediante medidas de tendencia central y representaciones gráficas que facilitan su interpretación.

---

## 1. Identificación del tipo de distribución de variables

Para analizar la forma en que se distribuyen los valores, se generaron diferentes tipos de gráficos según el contenido de cada hoja:

- **Clientes:** gráfico de torta para observar la distribución de clientes por ciudad.  
- **Detalle_Ventas:** histograma con líneas de referencia para visualizar la distribución de los importes.  
- **Productos:** boxplot que muestra la dispersión y rangos de precios por categoría.  
- **Ventas:** gráfico de barras para visualizar la frecuencia de los medios de pago utilizados.

### Ejemplo: Distribución del importe de ventas

```python
plt.figure(figsize=(8,5))
plt.hist(df_detalle['importe'], bins=15, color='skyblue', edgecolor='black', alpha=0.7)
plt.axvline(df_detalle['importe'].mean(), color='red', linestyle='--', linewidth=2, label='Media')
plt.axvline(df_detalle['importe'].median(), color='green', linestyle='--', linewidth=2, label='Mediana')
plt.axvline(df_detalle['importe'].mode()[0], color='orange', linestyle='--', linewidth=2, label='Moda')
plt.title("Distribución del Importe con Media, Mediana y Moda")
plt.xlabel("Importe")
plt.ylabel("Frecuencia")
plt.legend()
plt.show()
```

**Interpretación:**  
El histograma muestra que la variable *importe* está **concentrada en valores bajos y medios**, con una menor cantidad de ventas de alto valor.  
La diferencia entre la media, mediana y moda refleja una **distribución asimétrica hacia la derecha**, típica en datos de ventas.

---

## 2. Detección de outliers (valores extremos)

Para identificar posibles valores atípicos se utilizó el **boxplot de precios unitarios** por categoría de producto:

```python
plt.figure(figsize=(10,6))
sns.boxplot(x='categoria_general', y='precio_unitario', data=df_producto, hue='categoria_general', palette='Set3', legend=False)
plt.title('Distribución del Precio Unitario por Categoría de Producto')
plt.xlabel('Categoría General')
plt.ylabel('Precio Unitario')
plt.xticks(rotation=45)
plt.show()
```

**Interpretación:**  
Los valores atípicos se observan en forma de puntos fuera de los rangos principales del boxplot.  
Estos representan productos con precios considerablemente más altos o bajos que el resto de su categoría.  
Aunque no se eliminaron en esta etapa, sirven para detectar posibles errores de carga o productos especiales.

---

## 3. Gráficos representativos del análisis

Los gráficos más relevantes obtenidos en el proceso fueron:

1. **Gráfico de torta – Distribución de Clientes por Ciudad:** muestra la proporción de clientes según su ubicación.  
2. **Histograma – Distribución de Importes:** permite observar la tendencia central y dispersión de los montos de venta.  
3. **Boxplot – Precio Unitario por Categoría:** evidencia los rangos de precios y posibles valores atípicos.  
4. **Gráfico de barras – Medios de Pago Más Utilizados:** presenta la frecuencia de los distintos métodos de pago.

Estos gráficos permiten obtener una visión general clara de los datos antes de avanzar al modelado.

---

## 4. Interpretación de resultados orientada al problema

A partir del análisis realizado se pueden destacar las siguientes conclusiones:

- Los clientes se concentran mayormente en un grupo reducido de ciudades, lo que puede ayudar a definir estrategias comerciales focalizadas.  
- La mayoría de las ventas presenta importes bajos o medios, con algunos valores más elevados que podrían representar compras grandes o mayoristas.  
- El método de pago **efectivo** es el más frecuente, lo que abre la posibilidad de fomentar medios digitales.  
- La recategorización de productos permitió observar diferencias claras entre los precios promedio por categoría.  
- No se detectaron inconsistencias graves ni valores faltantes en las variables analizadas.

En resumen, el análisis confirma que la base de datos se encuentra **limpia, coherente y lista para su uso en etapas posteriores de análisis y modelado**.

## 👨‍💻 Autor
**EQUIPO 1**  
Proyecto académico desarrollado en colaboración con **IBM SkillsBuild** y **Guayerd**.