import math
import csv
import os
from utils import crear_carpeta

def calcular_tamano_lote(d, k, c1, Sp, volumen_unitario, volumen_maximo, b, monto_maximo):
    """
    Calcula el tamaño del lote, verificando el cumplimiento de las restricciones.

    Args (todos son float):
        d: Demanda del insumo (kg).
        k: Costo por orden ($).
        c1: Costo de mantenimiento ($).
        Sp: Stock de protección (kg).
        volumen_unitario: volumen que ocupa una unidad del insumo (m3).
        volumen_maximo: volumen máximo disponible para almacenar el insumo (m3).
        b: Costo unitario del insumo ($).
        monto_maximo: Monto máximo a inmovilizar permitido ($).

    Returns:
        float: Tamaño del lote ajustado.
    """
    q = math.sqrt((2 * d * k) / c1)
    while True:
        S = q + Sp
        volumen_total = S * volumen_unitario
        monto_total = S * b
        if volumen_total <= volumen_maximo and monto_total <= monto_maximo:
            break
        if volumen_total > volumen_maximo:
            q = (volumen_maximo / volumen_unitario) - Sp
        if monto_total > monto_maximo:
            q = (monto_maximo / b) - Sp
    return q

def calcular_variables(q, d, k, c1, b, Sp, duracion_temporada):
    """
    Calcula las variables del inventario (excepto q).

    Args (todos son float):
        q: Tamaño del lote (kg).
        d: Demanda del insumo (kg).
        k: Costo por orden ($).
        c1: Costo de mantenimiento ($).
        b: Costo de adquisición ($).
        Sp: Stock de protección (kg).
        duracion_temporada: Duración de la temporada (semanas).

    Returns:
        tupla: Variables calculadas (t, n_pedidos, D, S, CTE).
    """
    t = q / d
    n_pedidos = math.ceil(duracion_temporada / t)
    D = d * duracion_temporada
    S = q + Sp
    CTE = (D * k / q) + (q * c1 / 2) + (D * b) + (Sp * c1)
    return t, n_pedidos, D, S, CTE

def modelo_insumo(insumo, parametros, demanda, duracion_temporada, k):
    """
    Implementa el modelo para un insumo en una temporada, determinando el valor de las variables.

    Args:
        insumo (str): Nombre del insumo.
        parametros (dict): Parámetros del insumo.
        demanda (float): Demanda semanal del insumo ($).
        duracion_temporada (float): Duración de la temporada (semanas).
        k (float): Costo por orden ($).

    Returns:
        list: Resultados del procesamiento del insumo.
    """
    # Obtención de los valores de los parámetros
    b = parametros['b']
    c1 = parametros['c1']
    Sp = parametros['Sp']
    volumen_unitario = parametros['volumen_unitario']
    volumen_maximo = parametros['volumen_maximo']
    monto_maximo = parametros['monto_maximo']
    
    # Calcular variables
    q = calcular_tamano_lote(demanda, k, c1, Sp, volumen_unitario, volumen_maximo, b, monto_maximo)
    t, n_pedidos, D, S, CTE = calcular_variables(q, demanda, k, c1, b, Sp, duracion_temporada)
    volumen_total = S * volumen_unitario
    monto_total = S * b
    return [insumo, round(q, 2), round(t, 2), n_pedidos, round(D, 2), round(S, 2), round(CTE, 2), round(volumen_total, 2), round(monto_total, 2)]

def modelo_temporada(temporada, insumos, k, carpeta):
    """
    Implementa el modelo para todos los insumos durante una temporada.

    Args:
        temporada (dict): Información de la temporada.
        insumos (dict): Datos de los insumos.
        k (float): Costo por orden ($).
        carpeta (str): Carpeta donde se guardan los resultados.
    """
    nombre_temporada = temporada['nombre']
    duracion_temporada = temporada['duracion_temporada']
    demandas = temporada['demandas']
    archivo_csv = os.path.join(carpeta, f"temporada_{nombre_temporada}.csv")
    with open(archivo_csv, mode='w', newline='', encoding='utf-8') as archivo:
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerow(["Insumo", "q (kg)", "t (sem)", "n", "D", "S_max", "CTE", "Volumen ocupado (m³)", "Monto total inmovilizado ($)"])
        for insumo, parametros in insumos.items():
            demanda = demandas.get(insumo, 0)
            resultados = modelo_insumo(insumo, parametros, demanda, duracion_temporada, k)
            escritor_csv.writerow(resultados)

def modelo_inventario(insumos, k, temporadas, carpeta="inventory_plan"):
    """
    Implementa el modelo de inventario para varias temporadas.

    Args:
        insumos (dict): Datos de los insumos.
        k (float): Costo por orden ($).
        temporadas (list): Lista de temporadas.
        carpeta (str): Carpeta para guardar los resultados.
    """
    crear_carpeta(carpeta)
    for temporada in temporadas:
        modelo_temporada(temporada, insumos, k, carpeta)


# Parámetros para los insumos
insumos = {
    "Harina de Trigo": {"b": 1600, "c1": 685.12, "Sp": 120, "volumen_unitario": 0.0018, "volumen_maximo": 22, "monto_maximo": 2000000},
    "Azúcar": {"b": 1600, "c1": 685.12, "Sp": 4, "volumen_unitario": 0.0014, "volumen_maximo": 1.5, "monto_maximo": 90000},
    "Sal": {"b": 1600, "c1": 685.12, "Sp": 3, "volumen_unitario": 0.00075, "volumen_maximo": 1, "monto_maximo": 110000},
    "Manteca": {"b": 13000, "c1": 5566.6, "Sp": 12, "volumen_unitario": 0.0015, "volumen_maximo": 2.5, "monto_maximo": 800000}
}

# Parámetros por temporada
temporadas = [
    {"nombre": "1", "duracion_temporada": 14, "demandas": {"Harina de Trigo": 179.656, "Azúcar": 3.245, "Sal": 4.160, "Manteca": 19.907}},
    {"nombre": "2", "duracion_temporada": 20, "demandas": {"Harina de Trigo": 319.834, "Azúcar": 6.052, "Sal": 7.405, "Manteca": 22.662}},
    {"nombre": "3", "duracion_temporada": 7, "demandas": {"Harina de Trigo": 617.404, "Azúcar": 12.547, "Sal": 14.213, "Manteca": 44.75}},
    {"nombre": "4", "duracion_temporada": 11, "demandas": {"Harina de Trigo": 284.965, "Azúcar": 5.289, "Sal": 6.558, "Manteca": 22.052}}
]

# Otros parámetros constantes
k = 30000  # Costo por orden

# Ejecutar modelo
modelo_inventario(insumos, k, temporadas)
