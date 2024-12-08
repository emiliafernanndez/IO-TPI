import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de carpeta y subcarpeta de salida
output_dir_base = 'sensitivity'
output_dir = os.path.join(output_dir_base, 'q')
os.makedirs(output_dir, exist_ok=True)

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
    "Manteca": {"b": 13000, "c1": 5566.6, "Sp": 12},
}

# Tamaños de lote originales
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

def generar_qs(valor_original):
    """
    Genera 20 valores de q en el rango [q/4, q*4].

    Args:
        valor_original (float): Tamaño de lote original.

    Returns:
        np.ndarray: Array con 20 valores de q.
    """
    q_min = valor_original / 4
    q_max = valor_original * 4
    return np.linspace(q_min, q_max, 20)

def graficar_cte(df_resultados_q):
    """
    Genera gráficos comparando CTE y q para cada combinación de insumo y temporada.

    Args:
        df_resultados_q (pd.DataFrame): DataFrame con resultados de CTE.
    """
    for insumo in df_resultados_q["Insumo"].unique():
        for temporada in df_resultados_q["Temporada"].unique():
            
            # Filtrar datos para el insumo y temporada actuales
            df_filtrado = df_resultados_q[
                (df_resultados_q["Insumo"] == insumo) & 
                (df_resultados_q["Temporada"] == temporada)
            ]

            # Graficar
            plt.figure(figsize=(10, 6))
            plt.plot(df_filtrado["q"], df_filtrado["CTE"], marker='o', label=f'{insumo} - T{temporada}')
            plt.title(f'CTE vs q para {insumo} - Temporada {temporada}')
            plt.xlabel('Tamaño de lote (q)')
            plt.ylabel('CTE')
            plt.legend()
            plt.grid(True)

            # Guardar gráfico
            filename = f'{insumo}_{temporada}_sensitivity_q.png'.replace(" ", "_")
            plt.savefig(os.path.join(output_dir, filename), dpi=300, bbox_inches='tight')
            plt.close()

def main():
    """
    Función principal para realizar el análisis de sensibilidad en q.
    """
    resultados_q = {"Temporada": [], "Insumo": [], "q": [], "Demanda_Total": [], "CTE": []}

    # Generar valores de q y calcular CTE
    for temporada_info in temporadas:
        temporada = temporada_info["nombre"]
        duracion_temporada = temporada_info["duracion_temporada"]

        for insumo, demanda_media in temporada_info["demandas"].items():
            demanda_total = demanda_media * duracion_temporada
            q_values = generar_qs(valores_q[1][insumo])

            for q in q_values:
                # Calcular CTE
                cte = calcular_cte(
                    d=demanda_total,
                    k=30000,
                    q=q,
                    c1=insumos[insumo]["c1"],
                    b=insumos[insumo]["b"],
                    Sp=insumos[insumo]["Sp"]
                )

                # Guardar resultados
                resultados_q["Temporada"].append(temporada)
                resultados_q["Insumo"].append(insumo)
                resultados_q["q"].append(q)
                resultados_q["Demanda_Total"].append(demanda_total)
                resultados_q["CTE"].append(cte)

    # Convertir resultados a DataFrame
    df_resultados_q = pd.DataFrame(resultados_q)

    # Guardar resultados en CSV
    df_resultados_q.to_csv(f"{output_dir}/muestras_cte_q.csv", index=False)
    print(f"Resultados guardados en '{output_dir}/muestras_cte_q.csv'.")

    # Guardar estadísticas agrupadas
    agrupados_q = df_resultados_q.groupby(["Temporada", "Insumo"]).agg(
        Media_CTE=("CTE", "mean"),
        DE_CTE=("CTE", "std")
    ).reset_index()
    agrupados_q.to_csv(f"{output_dir}/cte_q_agrupados.csv", index=False)
    print(f"Estadísticas agrupadas guardadas en '{output_dir}/cte_q_agrupados.csv'.")

    # Generar gráficos
    graficar_cte(df_resultados_q)

if __name__ == "__main__":
    main()