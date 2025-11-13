# ============================================================
# PROYECTO AURELION – DEMO 1 + DEMO 2 (VERSIÓN CONSOLA)
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import webbrowser
from openpyxl import load_workbook
import os

# ============================================================
# RUTAS DE ARCHIVOS
# ============================================================

RUTA_EXCEL = "https://raw.githubusercontent.com/scovaleda/AURELION.Sprint2/main/BD_AURELION.xlsx"
RUTA_SALIDA = os.path.join(
    os.getcwd(),
    "BD_AURELION_LIMPIO.xlsx"
)


# ============================================================
# CARGA INICIAL DE DATOS
# ============================================================

def cargar_datos():
    df_cliente = pd.read_excel(RUTA_EXCEL, sheet_name="Clientes")
    df_detalle = pd.read_excel(RUTA_EXCEL, sheet_name="Detalle_Ventas")
    df_producto = pd.read_excel(RUTA_EXCEL, sheet_name="Productos")
    df_ventas = pd.read_excel(RUTA_EXCEL, sheet_name="Ventas")
    df_map = pd.read_excel(RUTA_EXCEL, sheet_name="Mapeo_Categorias")
    return df_cliente, df_detalle, df_producto, df_ventas, df_map

# ============================================================
# FUNCIONES DE LIMPIEZA + ANÁLISIS (DEMO 2)
# ============================================================

def limpiar_analizar_clientes(df_cliente, mostrar_graficos=True):
    filas_originales = len(df_cliente)
    nulos_totales = df_cliente.isnull().sum().sum()
    duplicados_iniciales = df_cliente.duplicated().sum()

    print("Registros nulos por columna en Clientes:")
    print(df_cliente.isnull().sum())

    columnas_redundantes = ['email', 'telefono']
    columnas_existentes = [col for col in columnas_redundantes if col in df_cliente.columns]
    if columnas_existentes:
        df_cliente = df_cliente.drop(columns=columnas_existentes)
        print(f"Columnas eliminadas: {columnas_existentes}\n")
    else:
        print("No había columnas redundantes para eliminar.\n")

    print("Tabla limpia de Clientes después de la limpieza:")
    print(df_cliente.head())
    print("DATASET BD AURELION")
    print("\n========= CLIENTES ===============")

    duplicados = df_cliente.duplicated().sum()
    if duplicados > 0:
        df_cliente = df_cliente.drop_duplicates()
        print("Duplicados eliminados.\n")

    moda_ciudad = df_cliente['ciudad'].mode()[0]
    print(f"La ciudad más frecuente es: {moda_ciudad}")
    print("====================================\n")

    filas_finales = len(df_cliente)
    resumen = {
        "filas_originales": filas_originales,
        "filas_finales": filas_finales,
        "duplicados_eliminados": duplicados_iniciales,
        "nulos_detectados": nulos_totales
    }

    if mostrar_graficos:
        conteo_ciudades = df_cliente['ciudad'].value_counts().reset_index()
        conteo_ciudades.columns = ['ciudad', 'cantidad']
        colores = ['#4C72B0', '#55A868', '#C44E52', '#8172B3', '#CCB974', '#64B5CD']
        plt.figure(figsize=(4, 4))
        plt.pie( conteo_ciudades['cantidad'], labels=conteo_ciudades['ciudad'], autopct='%1.0f%%', startangle=90, colors=colores[:len(conteo_ciudades)], wedgeprops={'width': 0.55, 'edgecolor': 'white'}, textprops={'fontsize': 8, 'color': 'black'} )
        plt.title('Distribución de Clientes por Ciudad', fontsize=10, pad=8)
        texto_resumen = ( f"Filas originales: {resumen['filas_originales']}\n" f"Filas finales: {resumen['filas_finales']}\n" f"Duplicados eliminados: {resumen['duplicados_eliminados']}\n" f"Nulos detectados: {resumen['nulos_detectados']}\n" f"Moda ciudad: {moda_ciudad}" )
        plt.figtext( 0.1, 0.01, "Cada segmento indica el porcentaje\n" "de registros de clientes en cada ubicación.\n\n" + texto_resumen, ha="left", fontsize=8, color='black' )
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    return df_cliente, resumen

def limpiar_analizar_productos(df_producto, df_map, mostrar_graficos=True):
    filas_originales = len(df_producto)
    nulos_totales = df_producto.isnull().sum().sum()
    duplicados_iniciales = df_producto.duplicated().sum()

    print("Registros nulos por columna en Productos:")
    print(df_producto.isnull().sum())

    columnas_redundantes = ['categoria']
    columnas_existentes = [col for col in columnas_redundantes if col in df_producto.columns]
    if columnas_existentes:
        df_producto = df_producto.drop(columns=columnas_existentes)
        print(f"Columnas eliminadas: {columnas_existentes}\n")
    else:
        print("No había columnas redundantes para eliminar.\n")

    duplicados = df_producto.duplicated().sum()
    if duplicados > 0:
        df_producto = df_producto.drop_duplicates()
        print("Duplicados eliminados.\n")

    if "stock_actual" not in df_producto.columns:
        np.random.seed(42)
        df_producto["stock_actual"] = np.random.randint(10, 31, size=len(df_producto))

    media_producto = df_producto['precio_unitario'].mean()
    mediana_producto = df_producto['precio_unitario'].median()
    moda_producto = df_producto['precio_unitario'].mode()[0]
    print(f"El precio promedio es: {media_producto}")
    print(f"El precio central: {mediana_producto}")
    print(f"El precio más frecuente es: {moda_producto}\n")

    df_map['palabra_clave'] = df_map['palabra_clave'].str.lower().str.strip()
    df_map = df_map.sort_values(by="prioridad")

    def clasificar_producto(nombre_producto):
        if pd.isna(nombre_producto):
            return "Otros"
        nombre = str(nombre_producto).lower()
        for _, fila in df_map.iterrows():
            palabra = fila['palabra_clave']
            categoria = fila['categoria_general']
            if palabra in nombre:
                return categoria
        return "Otros"

    df_producto['categoria_general'] = df_producto['nombre_producto'].apply(clasificar_producto)

    df_producto = df_producto[['id_producto', 'nombre_producto', 'categoria_general', 'precio_unitario', 'stock_actual']]

    print("=============================================================")
    print("DataFrame limpio actualizado en memoria (Productos):")
    print(df_producto.head())
    print("-------------------------------------------------------------")

    filas_finales = len(df_producto)
    resumen = {
        "filas_originales": filas_originales,
        "filas_finales": filas_finales,
        "duplicados_eliminados": duplicados_iniciales,
        "nulos_detectados": nulos_totales,
        "media_precio": media_producto,
        "mediana_precio": mediana_producto,
        "moda_precio": moda_producto
    }

    if mostrar_graficos:
        plt.figure(figsize=(6, 3.2))
        colores = ['#4C72B0', '#55A868', '#C44E52', '#8172B3', '#CCB974', '#64B5CD']

        sns.boxplot(
            x='categoria_general',
            y='precio_unitario',
            data=df_producto,
            palette=colores,
            linewidth=0.8,
            fliersize=2
        )

        plt.title('Distribución del Precio Unitario por Categoría de Producto', fontsize=10, pad=8)
        plt.xlabel('Categoría General', fontsize=8)
        plt.ylabel('Precio Unitario', fontsize=8)
        plt.xticks(rotation=30, fontsize=7)
        plt.yticks(fontsize=7)
        plt.grid(axis='y', linestyle='--', alpha=0.3)

        texto_resumen = (
            f"Filas originales: {resumen['filas_originales']} | "
            f"Filas finales: {resumen['filas_finales']} | "
            f"Duplicados elim.: {resumen['duplicados_eliminados']}\n"
            f"Nulos detectados: {resumen['nulos_detectados']} | "
            f"Media: {media_producto:.2f} | "
            f"Mediana: {mediana_producto:.2f} | "
            f"Moda: {moda_producto:.2f}"
        )

        plt.figtext(
            0.5, 0.1, 
            "El gráfico muestra la dispersión y mediana de los precios unitarios en cada categoría de producto.\n"
            "Facilita comparar rangos de precios y detectar posibles valores atípicos.\n\n" + texto_resumen,
            ha='center',
            fontsize=7,
            color='black'
        )

        plt.tight_layout()
        plt.show()

    return df_producto, resumen


def limpiar_analizar_ventas(df_ventas, mostrar_graficos=True):
    filas_originales = len(df_ventas)
    nulos_totales = df_ventas.isnull().sum().sum()
    duplicados_iniciales = df_ventas.duplicated().sum()

    print("Registros nulos por columna en ventas:")
    print(df_ventas.isnull().sum())
    print("\n================================= VENTAS ===================================")

    duplicados = df_ventas.duplicated().sum()
    if duplicados > 0:
        df_ventas = df_ventas.drop_duplicates()
        print("Duplicados eliminados.\n")

    moda_ventas = df_ventas['medio_pago'].mode()[0]
    print(f"El medio de pago más utilizado es: {moda_ventas}\n")

    columnas_redundantes = ['nombre_cliente', 'email']
    columnas_existentes = [col for col in columnas_redundantes if col in df_ventas.columns]
    if columnas_existentes:
        df_ventas = df_ventas.drop(columns=columnas_existentes)
        print(f"Columnas eliminadas: {columnas_existentes}\n")
    else:
        print("No había columnas redundantes para eliminar.\n")

    print("DataFrame limpio actualizado en memoria (Ventas):")
    print(df_ventas.head())
    print("============================================================================")

    filas_finales = len(df_ventas)
    resumen = {
        "filas_originales": filas_originales,
        "filas_finales": filas_finales,
        "duplicados_eliminados": duplicados_iniciales,
        "nulos_detectados": nulos_totales,
        "moda_medio_pago": moda_ventas
    }

    if mostrar_graficos:
        conteo_medios_pago = df_ventas['medio_pago'].value_counts()

        plt.figure(figsize=(7.5, 4.2))
        colores = ['#4C72B0', '#55A868', '#C44E52', '#8172B3', '#CCB974', '#64B5CD']

        sns.barplot(
            x=conteo_medios_pago.index,
            y=conteo_medios_pago.values,
            palette=colores,
            edgecolor='white',
            width=0.5
        )

        plt.plot(
            np.arange(len(conteo_medios_pago)),
            conteo_medios_pago.values,
            color='gray',
            linestyle='--',
            marker='o',
            markersize=4,
            linewidth=1
        )

        plt.title('Medios de Pago Más Utilizados', fontsize=10, pad=8)
        plt.xlabel('Medio de Pago', fontsize=8)
        plt.ylabel('Cantidad de Ventas', fontsize=8)
        plt.xticks(rotation=20, fontsize=7)
        plt.yticks(fontsize=7)
        plt.grid(axis='y', linestyle='--', alpha=0.3)

        texto_resumen = (
            f"Filas originales: {resumen['filas_originales']} | "
            f"Filas finales: {resumen['filas_finales']} | "
            f"Duplicados elim.: {resumen['duplicados_eliminados']} | "
            f"Nulos detectados: {resumen['nulos_detectados']}\n"
            f"Moda medio de pago: {moda_ventas}"
        )

        plt.figtext(
            0.5, -0.01,
            "El gráfico combina barras y una línea de tendencia para mostrar la distribución del uso de los medios de pago.\n"
            "Permite observar las preferencias de los clientes y variaciones en la frecuencia de uso.\n\n" + texto_resumen,
            ha='center',
            fontsize=7,
            color='black'
        )

        plt.tight_layout()
        plt.show()

    return df_ventas, resumen


def limpiar_analizar_detalle(df_detalle, mostrar_graficos=True):
    filas_originales = len(df_detalle)
    nulos_totales = df_detalle.isnull().sum().sum()
    duplicados_iniciales = df_detalle.duplicated().sum()

    print("\n==================== DETALLE DE VENTAS ============================")
    print("Registros nulos por columna en Detalle_Ventas:")
    print(df_detalle.isnull().sum())

    duplicados = df_detalle.duplicated().sum()
    if duplicados > 0:
        df_detalle = df_detalle.drop_duplicates()
        print("Duplicados eliminados.\n")

    media_detalle_ventas = df_detalle['importe'].mean()
    mediana_detalle_ventas = df_detalle['importe'].median()
    moda_detalle_ventas = df_detalle['importe'].mode()[0]
    print(f"El importe promedio es: {media_detalle_ventas}")
    print(f"El importe central: {mediana_detalle_ventas}")
    print(f"El importe más frecuente es: {moda_detalle_ventas}\n")

    columnas_redundantes = ['nombre_producto', 'precio_unitario']
    columnas_existentes = [col for col in columnas_redundantes if col in df_detalle.columns]
    if columnas_existentes:
        df_detalle = df_detalle.drop(columns=columnas_existentes)
        print(f"Columnas eliminadas: {columnas_existentes}\n")
    else:
        print("No había columnas redundantes para eliminar.\n")

    print("DataFrame limpio actualizado en memoria (Detalle_Ventas):")
    print(df_detalle.head())
    print("===================================================================")

    filas_finales = len(df_detalle)
    resumen = {
        "filas_originales": filas_originales,
        "filas_finales": filas_finales,
        "duplicados_eliminados": duplicados_iniciales,
        "nulos_detectados": nulos_totales,
        "media_importe": media_detalle_ventas,
        "mediana_importe": mediana_detalle_ventas,
        "moda_importe": moda_detalle_ventas
    }

    if mostrar_graficos:
        fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

        axes[0].hist(
            df_detalle['importe'],
            bins=15,
            color='#4C72B0',
            edgecolor='white',
            alpha=0.8
        )

        axes[0].axvline(df_detalle['importe'].mean(), color='red', linestyle='--', linewidth=1.5, label='Media')
        axes[0].axvline(df_detalle['importe'].median(), color='green', linestyle='--', linewidth=1.5, label='Mediana')
        axes[0].axvline(df_detalle['importe'].mode()[0], color='orange', linestyle='--', linewidth=1.5, label='Moda')

        axes[0].set_title("Distribución del Importe (Media, Mediana y Moda)", fontsize=9, pad=6)
        axes[0].set_xlabel("Importe", fontsize=8)
        axes[0].set_ylabel("Frecuencia", fontsize=8)
        axes[0].legend(fontsize=7)
        axes[0].grid(axis='y', linestyle='--', alpha=0.3)

        df_corr = df_detalle[["cantidad", "importe"]].corr()

        sns.heatmap(
            df_corr,
            annot=True,
            cmap="coolwarm",
            fmt=".2f",
            ax=axes[1],
            cbar_kws={'shrink': 0.7}
        )

        axes[1].set_title("Matriz de Correlación - Detalle de Ventas", fontsize=9, pad=6)
        axes[1].tick_params(axis='x', labelrotation=20, labelsize=8)
        axes[1].tick_params(axis='y', labelrotation=0, labelsize=8)

        texto_resumen = (
            f"Filas originales: {resumen['filas_originales']} | "
            f"Filas finales: {resumen['filas_finales']} | "
            f"Duplicados elim.: {resumen['duplicados_eliminados']} | "
            f"Nulos detectados: {resumen['nulos_detectados']}\n"
            f"Media importe: {media_detalle_ventas:.2f} | "
            f"Mediana: {mediana_detalle_ventas:.2f} | "
            f"Moda: {moda_detalle_ventas:.2f}"
        )

        fig.suptitle("Análisis del Detalle de Ventas", fontsize=10, fontweight='bold', y=-1.01)
        plt.figtext(
            0.5, -0.02,
            "Visualización conjunta: el histograma muestra la dispersión del importe y el mapa de calor refleja la correlación\n"
            "entre cantidad e importe para analizar patrones de comportamiento en las ventas.\n\n" + texto_resumen,
            ha='center',
            fontsize=7,
            color='black'
        )

        plt.tight_layout()
        plt.show()

    return df_detalle, resumen

# ============================================================
# EXPORTAR BD LIMPIA
# ============================================================

def exportar_bd_limpia(df_cliente, df_detalle, df_producto, df_ventas, df_map):
    df_cliente_limpio, _ = limpiar_analizar_clientes(df_cliente, mostrar_graficos=False)
    df_producto_limpio, _ = limpiar_analizar_productos(df_producto, df_map, mostrar_graficos=False)
    df_ventas_limpio, _ = limpiar_analizar_ventas(df_ventas, mostrar_graficos=False)
    df_detalle_limpio, _ = limpiar_analizar_detalle(df_detalle, mostrar_graficos=False)

    with pd.ExcelWriter(RUTA_SALIDA, engine="openpyxl") as writer:
        df_cliente_limpio.to_excel(writer, sheet_name="Clientes", index=False)
        df_producto_limpio.to_excel(writer, sheet_name="Productos", index=False)
        df_ventas_limpio.to_excel(writer, sheet_name="Ventas", index=False)
        df_detalle_limpio.to_excel(writer, sheet_name="Detalle_Ventas", index=False)
        df_map.to_excel(writer, sheet_name="Mapeo_Categorias", index=False)

    return RUTA_SALIDA

# ============================================================
# MENÚ CONSOLA (DEMO 1)
# ============================================================

def mostrar_menu():
    print("\n" + "=" * 60)
    print("        MENÚ PRINCIPAL – PROYECTO AURELION (CONSOLA)")
    print("=" * 60)
    print("1. CLIENTE – Limpieza y análisis")
    print("2. PRODUCTOS – Limpieza y análisis")
    print("3. VENTAS – Limpieza y análisis")
    print("4. DETALLE DE VENTA – Limpieza y análisis")
    print("5. documentacion.md")
    print("6. Exportar BD limpia")
    print("7. Salir")
    print("=" * 60)


def abrir_documentacion():
    enlace_github = (
        "https://github.com/scovaleda/AURELION.Sprint2/blob/main/documentacion%20(2).md"
    )
    print(f"\nAbriendo archivo de documentación en GitHub:\n{enlace_github}")
    try:
        webbrowser.open(enlace_github)
    except Exception as e:
        print(f"\nError al intentar abrir el enlace: {str(e)}")

# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():
    print("Accediendo a 'Proyecto Aurelion'...\n")

    df_cliente, df_detalle, df_producto, df_ventas, df_map = cargar_datos()

    while True:
        mostrar_menu()
        try:
            opcion = int(input("Seleccione una opción del menú (1-7): "))
        except ValueError:
            print("\nDebe ingresar un número válido.")
            continue

        if opcion == 1:
            print("\nUsted ha seleccionado la BD CLIENTES.")
            print("A continuación observará el proceso de limpieza y análisis...\n")
            df_cliente, _ = limpiar_analizar_clientes(df_cliente, mostrar_graficos=True)

        elif opcion == 2:
            print("\nUsted ha seleccionado la BD PRODUCTOS.")
            print("A continuación observará el proceso de limpieza y análisis...\n")
            df_producto, _ = limpiar_analizar_productos(df_producto, df_map, mostrar_graficos=True)

        elif opcion == 3:
            print("\nUsted ha seleccionado la BD VENTAS.")
            print("A continuación observará el proceso de limpieza y análisis...\n")
            df_ventas, _ = limpiar_analizar_ventas(df_ventas, mostrar_graficos=True)

        elif opcion == 4:
            print("\nUsted ha seleccionado la BD DETALLE DE VENTAS.")
            print("A continuación observará el proceso de limpieza y análisis...\n")
            df_detalle, _ = limpiar_analizar_detalle(df_detalle, mostrar_graficos=True)

        elif opcion == 5:
            abrir_documentacion()

        elif opcion == 6:
            print("\nUsted ha seleccionado EXPORTAR BD LIMPIA.")
            print("Se realizará la limpieza de todas las hojas y se exportará el archivo...\n")
            ruta = exportar_bd_limpia(df_cliente, df_detalle, df_producto, df_ventas, df_map)
            print(f"Base de datos limpia exportada correctamente en:\n{ruta}")

        elif opcion == 7:
            print("\nSaliendo del programa. Gracias por usar PROYECTO AURELION.")
            break

        else:
            print("\nOpción no válida. Por favor seleccione un número entre 1 y 7.")

if __name__ == "__main__":
    main()
