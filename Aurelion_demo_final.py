# ============================================================
# PROYECTO AURELION – DEMO 1 + DEMO 2 + SPRINT 3 (CONSOLA)
# ============================================================

import os
from pathlib import Path
from math import sqrt

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import webbrowser

from openpyxl import load_workbook

# --- ML / MODELOS ---
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingRegressor, RandomForestClassifier
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, classification_report
)

# --- PDF (exportar modelo ML) ---
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ============================================================
# RUTAS DE ARCHIVOS
# ============================================================

# Usamos SIEMPRE la BD desde GitHub
RUTA_EXCEL = "https://raw.githubusercontent.com/scovaleda/AURELION.Sprint2/main/BD_AURELION_ENTRENABLE_final.xlsx"

RUTA_SALIDA = os.path.join(
    os.getcwd(),
    "BD_AURELION_LIMPIO.xlsx"
)

# ============================================================
# HELPERS UX – "VENTANAS" EN CONSOLA
# ============================================================

def limpiar_pantalla():
    """Simula una nueva ventana en la consola."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar_y_volver(mensaje="\nPresione ENTER para volver al menú..."):
    """Pausa para que el usuario lea y luego limpia la pantalla."""
    input(mensaje)
    limpiar_pantalla()

# ============================================================
# CARGA INICIAL DE DATOS (DEMO 1 / DEMO 2)
# ============================================================

def cargar_datos():
    df_cliente = pd.read_excel(RUTA_EXCEL, sheet_name="Clientes")
    df_detalle = pd.read_excel(RUTA_EXCEL, sheet_name="Detalle_Ventas")
    df_producto = pd.read_excel(RUTA_EXCEL, sheet_name="Productos")
    df_ventas = pd.read_excel(RUTA_EXCEL, sheet_name="Ventas")
    df_map = pd.read_excel(RUTA_EXCEL, sheet_name="Mapeo_Categorias")
    # El Dataset_Mensual se usa solo en Sprint 3 (se carga allá)
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

        plt.figure(figsize=(4.5, 4.5))
        plt.pie(
            conteo_ciudades['cantidad'],
            labels=conteo_ciudades['ciudad'],
            autopct='%1.0f%%',
            startangle=90,
            colors=colores[:len(conteo_ciudades)],
            wedgeprops={'width': 0.55, 'edgecolor': 'white'},
            textprops={'fontsize': 8, 'color': 'black'}
        )
        plt.title('Distribución de Clientes por Ciudad', fontsize=10, pad=8)

        texto_resumen = (
            f"Filas originales: {resumen['filas_originales']}\n"
            f"Filas finales: {resumen['filas_finales']}\n"
            f"Duplicados eliminados: {resumen['duplicados_eliminados']}\n"
            f"Nulos detectados: {resumen['nulos_detectados']}\n"
            f"Moda ciudad: {moda_ciudad}"
        )

        plt.figtext(
            0.05, 0.01,
            "Cada segmento indica el porcentaje\n"
            "de registros de clientes en cada ubicación.\n\n" + texto_resumen,
            ha="left",
            fontsize=8,
            color='black'
        )
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
        plt.figure(figsize=(6.5, 3.5))
        colores = ['#4C72B0', '#55A868', '#C44E52', '#8172B3', '#CCB974', '#64B5CD']

        sns.boxplot(
            x='categoria_general',
            y='precio_unitario',
            data=df_producto,
            palette=colores,
            linewidth=0.8,
            fliersize=2
        )

        plt.title('Precio Unitario por Categoría de Producto', fontsize=10, pad=8)
        plt.xlabel('Categoría General', fontsize=8)
        plt.ylabel('Precio Unitario', fontsize=8)
        plt.xticks(rotation=25, fontsize=7)
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
            0.5, 0.04,
            "La gráfica muestra la dispersión y mediana de los precios por categoría.\n"
            "Ayuda a identificar rangos típicos y posibles valores atípicos.\n\n" + texto_resumen,
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
            "El gráfico combina barras y una línea de tendencia para mostrar la distribución\n"
            "del uso de los medios de pago y las preferencias de los clientes.\n\n" + texto_resumen,
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

        fig.suptitle("Análisis del Detalle de Ventas", fontsize=10, fontweight='bold', y=-0.02)
        plt.figtext(
            0.5, -0.08,
            "El histograma muestra la dispersión del importe, y el mapa de calor refleja la correlación\n"
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
# SPRINT 3 – MODELOS ML AURELION (Con UX Mejorada)
# ============================================================

# Variables globales del contexto ML
_sprint3_inicializado = False

df_prod_ml = None
df_detalle_ml = None
df_mensual_ml = None
df_ml = None

modelo_reg = None
X_train = X_test = y_train = y_test = y_pred = None
q1 = q2 = None
df_clf = None

# ============================================================
# PREPROCESADOR – columnas numéricas y categóricas
# ============================================================

def build_preprocessor():
    num_cols = [
        "anio", "mes", "precio_unitario", "costo_producto",
        "margen_ganancia", "porcentaje_margen",
        "stock_actual", "stock_minimo"
    ]
    cat_cols = ["categoria_general"]

    return ColumnTransformer(
        [
            ("num", StandardScaler(), num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
        ]
    )

# ============================================================
# INICIALIZACIÓN COMPLETA DEL SPRINT 3 (solo 1 vez)
# ============================================================

def inicializar_sprint3():
    """
    Prepara todo el contexto ML:
    - Carga BD (Productos, Detalle, Dataset Mensual)
    - Merge
    - Limpieza
    - Preprocesamiento
    - Entrenamiento modelo de regresión
    - Métricas
    - Clasificación en TOP / MEDIO / BAJO
    """

    global _sprint3_inicializado
    global df_prod_ml, df_detalle_ml, df_mensual_ml, df_ml
    global modelo_reg, X_train, X_test, y_train, y_test, y_pred
    global q1, q2, df_clf

    if _sprint3_inicializado:
        return

    print("\nInicializando contexto de Machine Learning (Sprint 3)...")

    # --- 1. CARGA DE DATOS ---
    df_prod_ml = pd.read_excel(RUTA_EXCEL, sheet_name="Productos")
    df_detalle_ml = pd.read_excel(RUTA_EXCEL, sheet_name="Detalle_Ventas")
    df_mensual_ml = pd.read_excel(RUTA_EXCEL, sheet_name="Dataset_Mensual")

    # Normalizar nombres
    if "id_product" in df_mensual_ml.columns:
        df_mensual_ml = df_mensual_ml.rename(columns={"id_product": "id_producto"})
    if "id_product" in df_detalle_ml.columns:
        df_detalle_ml = df_detalle_ml.rename(columns={"id_product": "id_producto"})

    # --- 2. MERGE PRINCIPAL ---
    df_ml = df_mensual_ml.merge(
        df_prod_ml[
            [
                "id_producto", "nombre_producto", "categoria_general",
                "precio_unitario", "costo_producto",
                "margen_ganancia", "porcentaje_margen",
                "stock_actual", "stock_minimo"
            ]
        ],
        on="id_producto",
        how="left"
    )

    df_ml = df_ml.dropna().copy()

    df_ml["porcentaje_margen"] = (
        df_ml["porcentaje_margen"]
        .astype(str)
        .str.replace("%", "")
        .str.replace(",", ".")
        .astype(float)
    )

    # --- 3. MODELO DE REGRESIÓN ---
    X_cols = [
        "anio", "mes", "categoria_general", "precio_unitario",
        "costo_producto", "margen_ganancia",
        "porcentaje_margen", "stock_actual", "stock_minimo"
    ]
    y_col = "cantidad"

    X = df_ml[X_cols]
    y = df_ml[y_col]

    modelo_reg = Pipeline(
        [
            ("prep", build_preprocessor()),
            ("gbr", GradientBoostingRegressor(
                n_estimators=200,
                learning_rate=0.05,
                max_depth=5,
                subsample=0.9,
                random_state=42
            ))
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    modelo_reg.fit(X_train, y_train)
    y_pred = modelo_reg.predict(X_test)

    # --- Mostrar métricas en consola ---
    mae = mean_absolute_error(y_test, y_pred)
    rmse = sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print("\n=== MÉTRICAS MODELO REGRESIÓN ===")
    print(f"MAE  : {mae:.4f}")
    print(f"RMSE : {rmse:.4f}")
    print(f"R²   : {r2:.4f}")

    # --- 4. CLASIFICACIÓN ---
    q1 = y_train.quantile(0.30)
    q2 = y_train.quantile(0.80)

    df_clf = df_ml.copy()

    df_clf["nivel_ventas"] = np.select(
        [df_clf[y_col] >= q2, df_clf[y_col] <= q1],
        ["TOP", "BAJO"],
        default="MEDIO"
    )

    df_clf["riesgo_stock"] = df_clf.apply(
        lambda row: (
            "ALTO_RIESGO" if row["stock_actual"] < row["stock_minimo"]
            else "MEDIO_RIESGO" if row["stock_actual"] < row["stock_minimo"] * 1.5
            else "SIN_RIESGO"
        ),
        axis=1
    )

    _sprint3_inicializado = True
    print("\nContexto ML del Sprint 3 inicializado correctamente.\n")

# ============================================================
# FUNCIÓN UNIVERSAL PARA TEXTO DE INTERPRETACIÓN EN GRÁFICAS
# ============================================================

def agregar_interpretacion(texto):
    plt.gca().text(
        1.02, 0.98, texto,
        transform=plt.gca().transAxes,
        fontsize=9,
        va="top",
        bbox=dict(
            facecolor="white",
            alpha=0.85,
            edgecolor="gray"
        )
    )

# ============================================================
# 5.1 – TOP 20 PRODUCTOS CON MAYOR DEMANDA (REAL)
# ============================================================

def sprint3_top20():
    inicializar_sprint3()
    limpiar_pantalla()

    print("📊 TOP 20 PRODUCTOS CON MAYOR DEMANDA (REAL)\n")

    df_demand = (
        df_detalle_ml.groupby("id_producto")["cantidad"]
        .sum()
        .reset_index()
        .merge(df_prod_ml[["id_producto", "nombre_producto"]],
               on="id_producto", how="left")
        .sort_values("cantidad", ascending=False)
        .head(20)
    )

    producto_mayor_demanda = df_demand.iloc[0]

    plt.style.use("seaborn-v0_8-talk")

    plt.figure(figsize=(15, 6))
    plt.bar(df_demand["nombre_producto"], df_demand["cantidad"],
            color="#1f77b4", edgecolor="black")

    plt.ylabel("Cantidad vendida (unidades)", fontsize=12)
    plt.title("Top 20 Productos con Mayor Demanda (Real)",
              fontsize=14, fontweight="bold")

    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.grid(axis="y", alpha=0.25)

    # Etiquetas encima de cada barra
    max_val = df_demand["cantidad"].max()

    for idx, valor in enumerate(df_demand["cantidad"]):
        plt.text(
            idx,
            valor + max_val * 0.015,
            str(int(valor)),
            ha="center",
            va="bottom",
            fontsize=8,
            fontweight="bold"
        )

    # Cuadro interpretativo
    agregar_interpretacion(
        f"Producto más vendido:\n- {producto_mayor_demanda['nombre_producto']}\n"
        f"- {int(producto_mayor_demanda['cantidad'])} unidades"
    )

    plt.tight_layout()
    plt.show()

    print("\nProducto con MAYOR DEMANDA:")
    print(f"➡ {producto_mayor_demanda['nombre_producto']} – "
          f"{int(producto_mayor_demanda['cantidad'])} unidades\n")

    pausar_y_volver()
# ============================================================
# 5.2 – PREDICCIÓN TENDENCIA MENSUAL + DICIEMBRE
# ============================================================

def sprint3_prediccion_diciembre():
    inicializar_sprint3()
    limpiar_pantalla()

    print("📈 TENDENCIA MENSUAL + PREDICCIÓN DICIEMBRE\n")

    df_mes = (
        df_mensual_ml.groupby(["anio", "mes"])
        .agg(
            cantidad_total=("cantidad", "sum"),
            precio_promedio=("precio", "mean"),
            costo_promedio=("costo", "mean")
        )
        .reset_index()
    )

    df_mes["fecha"] = pd.to_datetime(
        df_mes["anio"].astype(str) + "-" + df_mes["mes"].astype(str) + "-01"
    )
    df_mes = df_mes.sort_values("fecha")
    df_mes["mes_num"] = np.arange(1, len(df_mes) + 1)
    df_mes["rolling_3"] = df_mes["cantidad_total"].rolling(3).mean().bfill()

    X_m = df_mes[["mes_num", "rolling_3", "precio_promedio", "costo_promedio"]]
    y_m = df_mes["cantidad_total"]

    X_m_train, X_m_test, y_m_train, y_m_test = train_test_split(
        X_m, y_m, test_size=0.2, random_state=42
    )

    modelo_mensual = GradientBoostingRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=4,
        subsample=0.9,
        random_state=42
    )
    modelo_mensual.fit(X_m_train, y_m_train)

    anio_pred = df_mes["anio"].max()
    fecha_dic_pred = pd.to_datetime(f"{anio_pred}-12-01")

    rolling_pred = df_mes["cantidad_total"].tail(3).mean()

    X_future = pd.DataFrame({
        "mes_num": [df_mes["mes_num"].iloc[-1] + 1],
        "rolling_3": [rolling_pred],
        "precio_promedio": [df_mes["precio_promedio"].mean()],
        "costo_promedio": [df_mes["costo_promedio"].mean()]
    })

    pred_dic = modelo_mensual.predict(X_future)[0]

    print(f"🔮 Predicción diciembre {anio_pred}: {int(pred_dic)} unidades estimadas\n")

    plt.style.use("seaborn-v0_8-talk")
    plt.figure(figsize=(14, 6))

    fechas = df_mes["fecha"]
    cantidades = df_mes["cantidad_total"]

    # 1) Línea suavizada
    plt.plot(
        fechas,
        cantidades.rolling(3).mean(),
        color="#1f77b4",
        linewidth=2,
        label="Tendencia suavizada (rolling 3)"
    )

    # 2) Picos alto y bajo
    pico_alto = df_mes.loc[df_mes["cantidad_total"].idxmax()]
    pico_bajo = df_mes.loc[df_mes["cantidad_total"].idxmin()]

    plt.scatter(pico_alto["fecha"], pico_alto["cantidad_total"],
                color="green", s=140, label="Pico alto", zorder=5)
    plt.scatter(pico_bajo["fecha"], pico_bajo["cantidad_total"],
                color="orange", s=140, label="Pico bajo", zorder=5)

    # Etiquetas resumidas (para evitar saturación)
    plt.text(
        pico_alto["fecha"],
        pico_alto["cantidad_total"] + 120,
        f"{pico_alto['fecha'].strftime('%Y-%m')}\n({int(pico_alto['cantidad_total'])})",
        color="green",
        fontsize=8,
        ha="center"
    )

    plt.text(
        pico_bajo["fecha"],
        pico_bajo["cantidad_total"] - 140,
        f"{pico_bajo['fecha'].strftime('%Y-%m')}\n({int(pico_bajo['cantidad_total'])})",
        color="orange",
        fontsize=8,
        ha="center"
    )

    # 3) Punto de predicción diciembre
    plt.scatter(
        fecha_dic_pred, pred_dic,
        color="red", s=160, label="Predicción diciembre"
    )

    plt.text(
        fecha_dic_pred,
        pred_dic + 130,
        f"{fecha_dic_pred.strftime('%Y-%m')}\n({int(pred_dic)})",
        color="red",
        fontsize=9,
        ha="center"
    )

    # 4) Tendencia lineal global
    X_tend = np.array([d.toordinal() for d in fechas]).reshape(-1, 1)
    y_tend = cantidades.values

    modelo_tend = LinearRegression()
    modelo_tend.fit(X_tend, y_tend)
    tend_line = modelo_tend.predict(X_tend)

    plt.plot(
        fechas, tend_line,
        color="black",
        linestyle="--",
        linewidth=1.8,
        label="Tendencia lineal"
    )

    # 5) Ticks cada 3 meses para evitar saturación
    fechas_xticks = list(fechas[::3])
    if fecha_dic_pred not in fechas_xticks:
        fechas_xticks.append(fecha_dic_pred)

    plt.xticks(fechas_xticks, rotation=45, ha="right", fontsize=8)

    plt.title("Tendencia Mensual de Ventas + Predicción Diciembre",
              fontsize=14, fontweight="bold")
    plt.ylabel("Cantidad vendida (unidades)")
    plt.grid(True, alpha=0.3)
    plt.legend()

    agregar_interpretacion(
        f"Predicción diciembre {anio_pred}:\n"
        f"- {int(pred_dic)} unidades estimadas\n"
        f"- Basado en tendencia histórica + rolling 3"
    )

    plt.tight_layout()
    plt.show()

    pausar_y_volver()


# ============================================================
# 5.3 – RIESGO DE DESABASTECIMIENTO (REGRESIÓN STOCK)
# ============================================================

def sprint3_stock_minimo():
    inicializar_sprint3()
    limpiar_pantalla()

    print("⚠ ANÁLISIS DE RIESGO DE DESABASTECIMIENTO\n")

    df_stock = df_prod_ml[df_prod_ml["stock_minimo"] > 0].copy()
    df_stock["ratio"] = df_stock["stock_actual"] / df_stock["stock_minimo"]

    df_risk = df_stock.sort_values("ratio").head(20).copy()
    producto_bajo_stock = df_risk.iloc[0]

    # True si está por debajo del mínimo
    df_risk["riesgo"] = df_risk["stock_actual"] < df_risk["stock_minimo"]

    plt.style.use("seaborn-v0_8-talk")
    plt.figure(figsize=(10, 7))

    x_vals = df_risk["stock_minimo"].values.reshape(-1, 1)
    y_vals = df_risk["stock_actual"].values

    modelo_lineal = LinearRegression()
    modelo_lineal.fit(x_vals, y_vals)

    x_line = np.linspace(x_vals.min(), x_vals.max(), 100).reshape(-1, 1)
    y_line = modelo_lineal.predict(x_line)

    # Línea de zona segura
    x_safe = np.linspace(x_vals.min(), x_vals.max(), 100)
    y_safe = x_safe

    plt.plot(
        x_safe, y_safe,
        color="#999999",
        linestyle=":",
        linewidth=2,
        label="Zona segura (stock actual = stock mínimo)"
    )

    # Puntos seguros
    plt.scatter(
        df_risk[df_risk["riesgo"] == False]["stock_minimo"],
        df_risk[df_risk["riesgo"] == False]["stock_actual"],
        color="#1f77b4",
        s=70,
        label="Stock suficiente"
    )

    # Puntos en riesgo
    plt.scatter(
        df_risk[df_risk["riesgo"] == True]["stock_minimo"],
        df_risk[df_risk["riesgo"] == True]["stock_actual"],
        color="#c0392b",
        s=90,
        label="Producto en riesgo"
    )

    # Etiquetas SOLO para los productos en riesgo (muy importantes)
    for _, row in df_risk[df_risk["riesgo"] == True].iterrows():
        plt.text(
            row["stock_minimo"] + 0.8,
            row["stock_actual"] + 0.8,
            row["nombre_producto"],
            fontsize=8,
            color="#7B0000"
        )

    # Línea de regresión
    plt.plot(
        x_line, y_line,
        color="black",
        linewidth=2,
        linestyle="--",
        label="Tendencia lineal"
    )

    plt.title("Relación Stock Mínimo vs Stock Actual (Regresión Lineal)",
              fontsize=14, fontweight="bold")
    plt.xlabel("Stock mínimo requerido")
    plt.ylabel("Stock actual disponible")
    plt.grid(alpha=0.25)
    plt.legend(fontsize=9)

    agregar_interpretacion(
        f"Producto más crítico:\n"
        f"- {producto_bajo_stock['nombre_producto']}\n"
        f"- Stock actual: {int(producto_bajo_stock['stock_actual'])}\n"
        f"- Mínimo requerido: {int(producto_bajo_stock['stock_minimo'])}"
    )

    plt.tight_layout()
    plt.show()

    print("\nProducto con BAJO STOCK (más crítico):")
    print(
        f"➡ {producto_bajo_stock['nombre_producto']} "
        f"(Actual: {int(producto_bajo_stock['stock_actual'])}, "
        f"Mínimo: {int(producto_bajo_stock['stock_minimo'])})\n"
    )

    pausar_y_volver()


# ============================================================
# 5.4 – PRODUCTOS TOP CON ALTA DEMANDA Y BAJO STOCK
# ============================================================

def sprint3_top_criticos():
    inicializar_sprint3()
    limpiar_pantalla()

    print("🔥 PRODUCTOS TOP CON ALTA DEMANDA Y BAJO STOCK\n")

    plt.style.use("seaborn-v0_8-talk")

    df_dem_stock = (
        df_clf.groupby(["id_producto", "nivel_ventas"])["cantidad"]
        .sum()
        .reset_index()
        .merge(
            df_prod_ml[["id_producto", "nombre_producto", "stock_actual", "stock_minimo"]],
            on="id_producto",
            how="left"
        )
    )

    df_top_crit = df_dem_stock[
        (df_dem_stock["nivel_ventas"] == "TOP") &
        (df_dem_stock["stock_minimo"] > 0) &
        (df_dem_stock["stock_actual"] < df_dem_stock["stock_minimo"] * 1.2)
    ].sort_values("cantidad", ascending=False).head(15)

    if len(df_top_crit) > 0:
        producto_critico = df_top_crit.iloc[0]
    else:
        producto_critico = None

    plt.figure(figsize=(14, 6))

    # Barras = demanda
    plt.bar(
        df_top_crit["nombre_producto"],
        df_top_crit["cantidad"],
        color="#27ae60",
        label="Demanda total (TOP)"
    )

    # Línea = stock actual
    plt.plot(
        df_top_crit["nombre_producto"],
        df_top_crit["stock_actual"],
        color="#c0392b",
        marker="o",
        linewidth=1.8,
        label="Stock actual"
    )

    # Línea = stock mínimo
    plt.plot(
        df_top_crit["nombre_producto"],
        df_top_crit["stock_minimo"],
        color="#7f8c8d",
        linestyle="--",
        linewidth=1.5,
        label="Stock mínimo"
    )

    plt.xticks(rotation=45, ha="right", fontsize=8)

    if not df_top_crit.empty:
        max_demanda = df_top_crit["cantidad"].max()

        # Etiquetas SOLO sobre barras de demanda
        for idx, val in enumerate(df_top_crit["cantidad"]):
            plt.text(
                idx,
                val + max_demanda * 0.015,
                str(int(val)),
                ha="center",
                va="bottom",
                fontsize=8,
                fontweight="bold"
            )

    plt.title("Productos TOP con Alta Demanda y Bajo Stock",
              fontsize=14, fontweight="bold")
    plt.ylabel("Unidades")
    plt.grid(axis="y", alpha=0.3)
    plt.legend(fontsize=9)

    if producto_critico is not None:
        agregar_interpretacion(
            "Producto TOP más crítico:\n"
            f"- {producto_critico['nombre_producto']}\n"
            f"- Demanda: {int(producto_critico['cantidad'])}\n"
            f"- Stock actual: {int(producto_critico['stock_actual'])}\n"
            f"- Stock mínimo: {int(producto_critico['stock_minimo'])}"
        )

    plt.tight_layout()
    plt.show()

    print("\nProducto TOP CRÍTICO:")
    if producto_critico is not None:
        print(
            f"➡ {producto_critico['nombre_producto']} | "
            f"Demanda: {int(producto_critico['cantidad'])}, "
            f"Stock: {int(producto_critico['stock_actual'])}, "
            f"Mínimo: {int(producto_critico['stock_minimo'])}\n"
        )
    else:
        print("No se encontraron productos TOP críticos.\n")

    pausar_y_volver()


# ============================================================
# 5.5 – MÉTRICAS / MATRIZ DE REGRESIÓN EN CONSOLA
# ============================================================

def mostrar_metricas_regresion():
    """
    Muestra en consola las métricas clave del modelo de regresión
    entrenado en inicializar_sprint3().
    """
    inicializar_sprint3()
    limpiar_pantalla()

    print("📐 MÉTRICAS DEL MODELO DE REGRESIÓN (DEMANDA MENSUAL)\n")

    # y_test y y_pred se llenan en inicializar_sprint3()
    mae = mean_absolute_error(y_test, y_pred)
    rmse = sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print(f"MAE  (Error absoluto medio)   : {mae:.4f}")
    print(f"RMSE (Raíz error cuadrático)  : {rmse:.4f}")
    print(f"R²   (Coeficiente de determinación): {r2:.4f}\n")

    print("Interpretación rápida:")
    print("- MAE: error medio en unidades de venta.")
    print("- RMSE: penaliza más los errores grandes.")
    print("- R² cercano a 1 indica buen poder explicativo.\n")

    pausar_y_volver()


# Alias para mantener compatibilidad con el menú antiguo
def matriz_regresion():
    mostrar_metricas_regresion()


# ============================================================
# 5.6 – EXPORTAR MODELO ML A PDF (CARPETA DESCARGAS)
# ============================================================

def exportar_modelo_ml():
    """
    Exporta un PDF sencillo con:
    - Métricas del modelo de regresión (MAE, RMSE, R²)
    - Breve resumen del modelo.
    El archivo se guarda en la carpeta Descargas del usuario:
        AURELION_ML_REPORTE.pdf
    """
    inicializar_sprint3()

    mae = mean_absolute_error(y_test, y_pred)
    rmse = sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    downloads = Path.home() / "Downloads"
    downloads.mkdir(parents=True, exist_ok=True)
    pdf_path = downloads / "AURELION_ML_REPORTE.pdf"

    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawString(72, height - 72, "PROYECTO AURELION – MODELO ML (REGRESIÓN)")

    c.setFont("Helvetica", 12)
    c.drawString(72, height - 110,
                 "Reporte automático de métricas del modelo de regresión.")
    c.line(72, height - 120, width - 72, height - 120)

    y_pos = height - 160
    c.setFont("Helvetica-Bold", 14)
    c.drawString(72, y_pos, "1. Métricas del modelo")
    y_pos -= 30
    c.setFont("Helvetica", 12)
    c.drawString(90, y_pos, f"• MAE  : {mae:.4f}")
    y_pos -= 20
    c.drawString(90, y_pos, f"• RMSE : {rmse:.4f}")
    y_pos -= 20
    c.drawString(90, y_pos, f"• R²   : {r2:.4f}")

    y_pos -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(72, y_pos, "2. Resumen del modelo")
    y_pos -= 25
    c.setFont("Helvetica", 11)
    c.drawString(90, y_pos, "El modelo Gradient Boosting estima la demanda mensual")
    y_pos -= 15
    c.drawString(90, y_pos, "usando año, mes, categoría, precio, costo, margen y stock.")
    y_pos -= 15
    c.drawString(90, y_pos, "Las métricas resumen el rendimiento sobre datos de prueba.")

    c.showPage()
    c.save()

    print(f"\n✅ Informe ML exportado correctamente en:\n{pdf_path}\n")
    pausar_y_volver()
# ============================================================
# FUNCIONES UX DE NAVEGACIÓN
# ============================================================

def limpiar_pantalla():
    """Limpia la consola en Windows, Mac o Linux."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar_y_volver():
    """Pausa la pantalla secundaria y regresa al menú que la llamó."""
    input("\nPresione ENTER para volver...")
    limpiar_pantalla()

    # ============================================================
# COLORES PARA LA CONSOLA (Colorama)
# ============================================================

try:
    from colorama import init, Fore, Style

    # Inicializar colorama (especialmente para Windows)
    init(autoreset=True)

    VERDE = Fore.GREEN
    AZUL = Fore.CYAN
    AMARILLO = Fore.YELLOW
    RESET = Style.RESET_ALL

except ImportError:
    # Si no está instalado colorama, usar cadenas vacías
    VERDE = ""
    AZUL = ""
    AMARILLO = ""
    RESET = ""

# ============================================================
# SUBMENÚ SPRINT 3 (Predicción + ML)
# ============================================================

def mostrar_submenu_sprint3():
    while True:
        limpiar_pantalla()
        print("=" * 60)
        print(VERDE + "    [🟢] SUBMENÚ – PREDICCIÓN DE DEMANDA E INVENTARIO" + RESET)
        print("=" * 60)

        print(AZUL + "\n[📊] ANÁLISIS PREDICTIVO" + RESET)
        print("  1. Mayor demanda – Top 20 productos")
        print("  2. Predicción – Ventas diciembre")

        print(AZUL + "\n[📉] RIESGOS E INVENTARIO" + RESET)
        print("  3. Stock mínimo – Riesgo de desabastecimiento")
        print("  4. Productos TOP críticos")

        print(AZUL + "\n[📈] MODELO DE REGRESIÓN" + RESET)
        print("  5. Métricas y matriz de regresión")

        print(AMARILLO + "\n[📝] EXPORTACIÓN" + RESET)
        print("  6. Exportar reporte ML en PDF")

        print("\n↩ 7. Volver al menú principal")
        print("=" * 60)

        try:
            op = int(input("Seleccione una opción (1-7): "))
        except ValueError:
            print("⚠ Debe ingresar un número válido.")
            continue

        if op == 1:
            sprint3_top20()
        elif op == 2:
            sprint3_prediccion_diciembre()
        elif op == 3:
            sprint3_stock_minimo()
        elif op == 4:
            sprint3_top_criticos()
        elif op == 5:
            mostrar_metricas_regresion()
        elif op == 6:
            exportar_modelo_ml()
        elif op == 7:
            limpiar_pantalla()
            break
        else:
            print("⚠ Opción incorrecta, intente nuevamente.")
            input("ENTER para continuar...")


# ============================================================
# DOCUMENTACIÓN DESDE GITHUB
# ============================================================

def abrir_documentacion():
    enlace_github = (
        "https://github.com/scovaleda/AURELION.Sprint2/blob/main/documentacion%20(2).md"
    )
    print(f"\nAbriendo archivo en GitHub:\n{enlace_github}")
    try:
        webbrowser.open(enlace_github)
    except Exception as e:
        print(f"\n⚠ Error al abrir el enlace: {str(e)}")
    pausar_y_volver()
    
# ============================================================
# SPRINT 4 - VISUALIZACIONES
# ============================================================

def visualizar_dashboard_powerbi():
    enlace_pdf = (
        "https://drive.google.com/file/d/1xV5cruZwFR6n7lbFfDMUP-eCMBbofEzR/view?usp=sharing"
    )
    print("\n🌐 Abriendo dashboard Power BI (PDF) en la web...")
    try:
        webbrowser.open(enlace_pdf)
    except Exception as e:
        print(f"\n⚠ Error al abrir el PDF: {str(e)}")
    pausar_y_volver()

def descargar_pbix_powerbi():
    enlace_pbix = (
        "https://drive.usercontent.google.com/u/0/uc?id=18YQBHtVzmsJ3j90Ls_gYl7KjGbYEOdca&export=download"
      
    )
    print("\n⬇ Iniciando descarga del archivo Power BI (.pbix)...")
    try:
        webbrowser.open(enlace_pbix)
    except Exception as e:
        print(f"\n⚠ Error al descargar el archivo: {str(e)}")
    pausar_y_volver()



# ============================================================
# MENÚ PRINCIPAL (VENTANA PRINCIPAL FIJA)
# ============================================================

def mostrar_menu():
    print("=" * 60)
    print(VERDE + "        MENÚ PRINCIPAL – PROYECTO AURELION (CONSOLA)" + RESET)
    print("=" * 60)

    print(AZUL + "\n[🔵] ANÁLISIS Y LIMPIEZA DE DATOS" + RESET)
    print("  1. CLIENTE")
    print("  2. PRODUCTOS")
    print("  3. VENTAS")
    print("  4. DETALLE DE VENTA")

    print(VERDE + "\n[🟢] MODELADO DE DATOS Y PREDICCIONES" + RESET)
    print("  5. Predicción de Demanda e Inventario")

    print(AMARILLO + "\n[🔶] UTILIDADES" + RESET)
    print("  6. Exportar BD limpia")
    print("  7. Abrir documentacion.md")

    print(AZUL + "\n[📊] VISUALIZACIONES POWER BI" + RESET)
    print("  8. Visualizar dashboard (PDF)")
    print("  9. Descargar archivo Power BI (.pbix)")

    print("\n 10. Salir")
    print("=" * 60)


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():
    limpiar_pantalla()
    print("Cargando Proyecto Aurelion...\n")

    df_cliente, df_detalle, df_producto, df_ventas, df_map = cargar_datos()

    while True:
        mostrar_menu()

        try:
            opcion = int(input("Seleccione una opción del menú (1-10): "))
        except ValueError:
            print("⚠ Debe ingresar un número válido.")
            input("ENTER para continuar...")
            limpiar_pantalla()
            continue

        # -----------------------------
        # ✔ ANALISIS Y LIMPIEZA (DEMO 2)
        # -----------------------------
        if opcion == 1:
            limpiar_pantalla()
            print("📂 Limpieza y análisis de CLIENTES\n")
            df_cliente, _ = limpiar_analizar_clientes(df_cliente, mostrar_graficos=True)
            pausar_y_volver()

        elif opcion == 2:
            limpiar_pantalla()
            print("📂 Limpieza y análisis de PRODUCTOS\n")
            df_producto, _ = limpiar_analizar_productos(df_producto, df_map, mostrar_graficos=True)
            pausar_y_volver()

        elif opcion == 3:
            limpiar_pantalla()
            print("📂 Limpieza y análisis de VENTAS\n")
            df_ventas, _ = limpiar_analizar_ventas(df_ventas, mostrar_graficos=True)
            pausar_y_volver()

        elif opcion == 4:
            limpiar_pantalla()
            print("📂 Limpieza y análisis de DETALLE DE VENTA\n")
            df_detalle, _ = limpiar_analizar_detalle(df_detalle, mostrar_graficos=True)
            pausar_y_volver()

        # -----------------------------
        # ✔ ML PREDICCIONES (SPRINT 3)
        # -----------------------------
        elif opcion == 5:
            mostrar_submenu_sprint3()

        # -----------------------------
        # ✔ EXPORTAR BD LIMPIA
        # -----------------------------
        elif opcion == 6:
            limpiar_pantalla()
            print("📤 Exportando BD limpia…")
            ruta = exportar_bd_limpia(df_cliente, df_detalle, df_producto, df_ventas, df_map)
            print(f"\n✔ Base de datos exportada en:\n{ruta}")
            pausar_y_volver()

        # -----------------------------
        # ✔ DOCUMENTACIÓN
        # -----------------------------
        elif opcion == 7:
            limpiar_pantalla()
            abrir_documentacion()

        elif opcion == 8:
            limpiar_pantalla()
            visualizar_dashboard_powerbi()

        elif opcion == 9:
            limpiar_pantalla()
            descargar_pbix_powerbi()

         # -----------------------------
        # ✔ SALIR
        # -----------------------------
        elif opcion == 10:
            print("\n⚠ Opción no válida. Seleccione un número del 1 al 10.")
            print("\nSaliendo del sistema. ¡Gracias por usar PROYECTO AURELION!")
            break
if __name__ == "__main__":
    main()
