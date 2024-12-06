import numpy as np
import pandas as pd

# Información de temporadas
temporadas = [
    {"nombre": "1", "duracion_temporada": 14, "demandas": {"Harina de Trigo": 179.656, "Azúcar": 3.245, "Sal": 4.160, "Manteca": 19.907}},
    {"nombre": "2", "duracion_temporada": 20, "demandas": {"Harina de Trigo": 319.834, "Azúcar": 6.052, "Sal": 7.405, "Manteca": 22.662}},
    {"nombre": "3", "duracion_temporada": 7, "demandas": {"Harina de Trigo": 617.404, "Azúcar": 12.547, "Sal": 14.213, "Manteca": 44.75}},
    {"nombre": "4", "duracion_temporada": 11, "demandas": {"Harina de Trigo": 284.965, "Azúcar": 5.289, "Sal": 6.558, "Manteca": 22.052}}
]

# Datos de los insumos
insumos = {
    "Harina de Trigo": {"b": 1600, "c1": 685.12, "Sp": 120},
    "Azúcar": {"b": 1600, "c1": 685.12, "Sp": 4},
    "Sal": {"b": 1600, "c1": 685.12, "Sp": 3},
    "Manteca": {"b": 13000, "c1": 5566.6, "Sp": 12}
}

# Tamaños de lote originales
valores_q = {
    1: {"Harina de Trigo": 469.3284, "Azúcar": 63.07593, "Sal": 71.41723, "Manteca": 54.80865},
    2: {"Harina de Trigo": 748.4618, "Azúcar": 102.9572, "Sal": 113.8859, "Manteca": 69.89478},
    3: {"Harina de Trigo": 615.2139, "Azúcar": 87.70286, "Sal": 93.34306, "Manteca": 58.10669},
    4: {"Harina de Trigo": 523.9430, "Azúcar": 71.38043, "Sal": 79.48412, "Manteca": 51.13275},
}

# Función para calcular CTE
def calcular_cte(d, k, q, c1, b, Sp):
    return (d * k / q) + (q * c1 / 2) + (d * b) + (Sp * c1)

# Generar 20 valores de q
def generar_qs(valor_original):
    q_min = valor_original / 4
    q_max = valor_original * 4
    return np.linspace(q_min, q_max, 20)

# Resultados
resultados_q = {"Temporada": [], "Insumo": [], "q": [], "Demanda_Total": [], "CTE": []}

# Generar valores de q y calcular CTE
for temporada_info in temporadas:
    temporada = temporada_info["nombre"]
    duracion_temporada = temporada_info["duracion_temporada"]
    
    for insumo, demanda_media in temporada_info["demandas"].items():
        demanda_total = demanda_media * duracion_temporada  # Demanda total ajustada por duración de la temporada
        q_values = generar_qs(valores_q[1][insumo])  # Generar los 20 valores de q

        for q in q_values:
            b = insumos[insumo]["b"]
            c1 = insumos[insumo]["c1"]
            Sp = insumos[insumo]["Sp"]
            k = 30000  # Costo por orden ($)

            # Calcular CTE
            cte = calcular_cte(demanda_total, k, q, c1, b, Sp)
            
            # Guardar resultados
            resultados_q["Temporada"].append(temporada)
            resultados_q["Insumo"].append(insumo)
            resultados_q["q"].append(q)
            resultados_q["Demanda_Total"].append(demanda_total)
            resultados_q["CTE"].append(cte)

# Convertir resultados a DataFrame para facilitar análisis
df_resultados_q = pd.DataFrame(resultados_q)

# Guardar todos los valores de q y CTE en un archivo CSV
df_resultados_q.to_csv("muestras_cte_q.csv", index=False)
print("Los valores de q y CTE se han guardado en 'muestras_cte_q.csv'.")

# Calcular media y desviación estándar del CTE agrupando por insumo, temporada y q
agrupados_q = df_resultados_q.groupby(["Temporada", "Insumo"]).agg(
    Media_CTE=("CTE", "mean"),
    DE_CTE=("CTE", "std")
).reset_index()

# Guardar los resultados agrupados en un archivo CSV
agrupados_q.to_csv("cte_q_agrupados.csv", index=False)
print("Los resultados agrupados por q se han guardado en 'cte_q_agrupados.csv'.")
