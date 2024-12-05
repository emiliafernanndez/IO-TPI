import numpy as np
import pandas as pd

# Datos de media y desviación estándar por insumo y temporada
data = {
    "Temporada": [1, 2, 3, 4],
    "Harina_Media": [179656.15, 319833.75, 617403.57, 284965.00],
    "Harina_DE": [94345.38, 117839.60, 112636.46, 90563.57],
    "Manteca_Media": [19906.92, 22661.75, 44750.00, 22051.82],
    "Manteca_DE": [5309.50, 10442.85, 11194.99, 6242.04],
    "Sal_Media": [4160.15, 7404.60, 14212.71, 6557.64],
    "Sal_DE": [2238.78, 2693.78, 2511.12, 2096.00],
    "Azúcar_Media": [3245.38, 6051.75, 12547.14, 5289.09],
    "Azúcar_DE": [1608.07, 2913.41, 3239.96, 2197.23],
}

# Crear DataFrame con los datos
df = pd.DataFrame(data)

# Datos de los insumos
insumos = {
    "Harina de Trigo": {"b": 1600, "c1": 685.12, "Sp": 120, "volumen_unitario": 0.0018, "volumen_maximo": 22, "monto_maximo": 2000000},
    "Azúcar": {"b": 1600, "c1": 685.12, "Sp": 4, "volumen_unitario": 0.0014, "volumen_maximo": 1.5, "monto_maximo": 90000},
    "Sal": {"b": 1600, "c1": 685.12, "Sp": 3, "volumen_unitario": 0.00075, "volumen_maximo": 1, "monto_maximo": 110000},
    "Manteca": {"b": 13000, "c1": 5566.6, "Sp": 12, "volumen_unitario": 0.0015, "volumen_maximo": 2.5, "monto_maximo": 800000}
}

# Configuración
muestras_por_temporada = 30  # Número de muestras a generar por temporada para cada insumo

# Generar muestras utilizando distribución normal
resultados = {"Temporada": [], "Insumo": [], "Muestra": [], "Demanda": [], "CTE": []}

# Función para calcular CTE
def calcular_cte(d, k, q, c1, b, Sp):
    return (d * k / q) + (q * c1 / 2) + (d * b) + (Sp * c1)

# Generar muestras
for index, row in df.iterrows():
    temporada = row["Temporada"]
    insumos_lista = ["Harina de Trigo", "Manteca", "Sal", "Azúcar"]
    
    for insumo in insumos_lista:
        media = row[f"{insumo.split()[0]}_Media"]
        desviacion = row[f"{insumo.split()[0]}_DE"]
        
        # Generar muestras para el insumo
        muestras = np.random.normal(loc=media, scale=desviacion, size=muestras_por_temporada)
        
        # Calcular CTE para cada muestra
        for muestra in muestras:
            # Extraer los parámetros específicos del insumo
            b = insumos[insumo]["b"]
            c1 = insumos[insumo]["c1"]
            Sp = insumos[insumo]["Sp"]
            q = 1000  # Tamaño de lote (kg)
            k = 30000  # Costo por orden ($)
            
            # Calcular CTE
            cte = calcular_cte(muestra, k, q, c1, b, Sp)
            
            # Guardar resultados
            resultados["Temporada"].append(temporada)
            resultados["Insumo"].append(insumo)
            resultados["Muestra"].append(len(resultados["Muestra"]) + 1)
            resultados["Demanda"].append(muestra)
            resultados["CTE"].append(cte)

# Convertir resultados a DataFrame para facilitar análisis
df_resultados = pd.DataFrame(resultados)

# Guardar los datos en un archivo CSV
df_resultados.to_csv("muestras_analisis_sensibilidad.csv", index=False)

print("Los datos se han guardado en 'muestras_cte.csv'")
