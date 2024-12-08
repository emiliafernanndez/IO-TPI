import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

# Configuración de carpeta y subcarpeta de salida
output_dir_base = 'sensitivity'
output_dir = os.path.join(output_dir_base, 'd')
os.makedirs(output_dir, exist_ok=True)

# Información de temporadas con media y D.E. de demanda
temporadas = [
    {
        "nombre": "1",
        "duracion_temporada": 14,
        "demandas": {
            "Harina de Trigo": {"media": 179.656, "de": 94.345},
            "Azúcar": {"media": 3.245, "de": 1.608},
            "Sal": {"media": 4.160, "de": 2.239},
            "Manteca": {"media": 19.907, "de": 5.310},
        },
    },
    {
        "nombre": "2",
        "duracion_temporada": 20,
        "demandas": {
            "Harina de Trigo": {"media": 319.834, "de": 117.840},
            "Azúcar": {"media": 6.052, "de": 2.913},
            "Sal": {"media": 7.405, "de": 2.694},
            "Manteca": {"media": 22.662, "de": 10.443},
        },
    },
    {
        "nombre": "3",
        "duracion_temporada": 7,
        "demandas": {
            "Harina de Trigo": {"media": 617.404, "de": 112.636},
            "Azúcar": {"media": 12.547, "de": 3.240},
            "Sal": {"media": 14.213, "de": 2.511},
            "Manteca": {"media": 44.750, "de": 11.195},
        },
    },
    {
        "nombre": "4",
        "duracion_temporada": 11,
        "demandas": {
            "Harina de Trigo": {"media": 284.965, "de": 90.564},
            "Azúcar": {"media": 5.289, "de": 2.197},
            "Sal": {"media": 6.558, "de": 2.096},
            "Manteca": {"media": 22.052, "de": 6.242},
        },
    },
]

# Datos de los insumos
insumos = {
    "Harina de Trigo": {"b": 1600, "c1": 685.12, "Sp": 120, "volumen_unitario": 0.0018, "volumen_maximo": 22, "monto_maximo": 2000000},
    "Azúcar": {"b": 1600, "c1": 685.12, "Sp": 4, "volumen_unitario": 0.0014, "volumen_maximo": 1.5, "monto_maximo": 90000},
    "Sal": {"b": 1600, "c1": 685.12, "Sp": 3, "volumen_unitario": 0.00075, "volumen_maximo": 1, "monto_maximo": 110000},
    "Manteca": {"b": 13000, "c1": 5566.6, "Sp": 12, "volumen_unitario": 0.0015, "volumen_maximo": 2.5, "monto_maximo": 800000},
}

# Tamaños de lote calculados previamente para cada temporada e insumo
valores_q = {
    1: {"Harina de Trigo": 469.3284, "Azúcar": 63.07593, "Sal": 71.41723, "Manteca": 54.80865},
    2: {"Harina de Trigo": 748.4618, "Azúcar": 102.9572, "Sal": 113.8859, "Manteca": 69.89478},
    3: {"Harina de Trigo": 615.2139, "Azúcar": 87.70286, "Sal": 93.34306, "Manteca": 58.10669},
    4: {"Harina de Trigo": 523.9430, "Azúcar": 71.38043, "Sal": 79.48412, "Manteca": 51.13275},
}

def calcular_cte(d, k, q, c1, b, Sp):
    """
    Calcula el Costo Total Esperado (CTE).
    Args (todos float):
        d: Demanda total de la temporada (kg).
        k: Costo de Orden ($).
        q: Tamaño del Lote (kg).
        c1: Costo unitario de Mantenimiento ($/kg).
        b: Costo unitario de Adquisición ($).
        Sp: Stock de Protección (kg).
    Returns:
        float: Costo total esperado.
    """
    return (d * k / q) + (q * c1 / 2) + (d * b) + (Sp * c1)

def generar_resultados(temporadas, insumos, valores_q, muestras_por_temporada):
    """
    Genera las simulaciones de CTE para cada combinación de temporada e insumo.
    """
    resultados = {"Temporada": [], "Insumo": [], "q": [], "Muestra": [], "Demanda_Total": [], "CTE": []}
    
    for temporada_info in temporadas:
        temporada = temporada_info["nombre"]
        duracion_temporada = temporada_info["duracion_temporada"]
        
        for insumo, datos in temporada_info["demandas"].items():
            demanda_media = datos["media"]
            desviacion = datos["de"]
            muestras = np.random.normal(loc=demanda_media, scale=desviacion, size=muestras_por_temporada)
            
            for q_id, valores in valores_q.items():
                q = valores[insumo]
                for i, muestra in enumerate(muestras):
                    
                    # Conseguir parámetros y calcular CTE
                    demanda_total = muestra * duracion_temporada
                    cte = calcular_cte(demanda_total, k=30000, q=q, c1=insumos[insumo]["c1"], b=insumos[insumo]["b"], Sp=insumos[insumo]["Sp"])
                    
                    # Guardar resultados
                    resultados["Temporada"].append(temporada)
                    resultados["Insumo"].append(insumo)
                    resultados["q"].append(q_id)
                    resultados["Muestra"].append(i + 1)
                    resultados["Demanda_Total"].append(demanda_total)
                    resultados["CTE"].append(cte)
    return pd.DataFrame(resultados)

def guardar_histogramas(df_resultados, output_dir):
    """
    Genera y guarda histogramas del CTE para cada combinación de temporada e insumo.
    """
    for temporada in df_resultados["Temporada"].unique():
        for insumo in df_resultados["Insumo"].unique():
            data = df_resultados[(df_resultados["Temporada"] == temporada) & (df_resultados["Insumo"] == insumo)]
            
            plt.figure(figsize=(10, 6))
            plt.hist(data["CTE"], bins=15, color='skyblue', edgecolor='black', alpha=0.7)
            plt.title(f"Histograma de Sensibilidad\nTemporada {temporada} - {insumo}")
            plt.xlabel("CTE (Costo Total Esperado)")
            plt.ylabel("Frecuencia")
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            
            filename = f"{insumo}_{temporada}_sensitivity_d.png".replace(" ", "_")
            filepath = os.path.join(output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()

# Configuración: muestras a generar por temporada para cada insumo
muestras_por_temporada = 50  

# Generar y guardar resultados
df_resultados = generar_resultados(temporadas, insumos, valores_q,muestras_por_temporada)
df_resultados.to_csv(f"{output_dir}/muestras_cte_d.csv", index=False)
print("Las muestras se han guardado en 'muestras_cte_d.csv'.")
   
# Calcular y guardar estadísticas agrupadas 
agrupados = df_resultados.groupby(["Temporada", "Insumo"]).agg(
    Media_CTE=("CTE", "mean"),
    DE_CTE=("CTE", "std")
).reset_index()
agrupados.to_csv(f"{output_dir}/cte_d_agrupados.csv", index=False)
print("Los resultados agrupados se han guardado en 'cte_d_agrupados.csv'.")
    
# Generar histogramas en .PNG
guardar_histogramas(df_resultados, output_dir)