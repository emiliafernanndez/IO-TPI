import math
import csv
import os
from utils import crear_carpeta

def calcular_variables(d, k, c1, b, Sp, duracion_temporada):
    """
    Calcula las variables del modelo de stock de protección.

    Args:
        nombre_temporada (str): Nombre de la temporada.
        datos_insumos (list): Lista de diccionarios con los datos de cada insumo necesarios para el cálculo.
        max_monto (float): Monto máximo permitido.
        max_volumen_sin (float): Volumen máximo sin refrigerar permitido.
        max_volumen_ref (float): Volumen máximo refrigerado permitido.
        carpeta (str): Carpeta donde guardar el archivo de texto.
        
    Returns:
        tupla: Variables calculadas (q, t, n_pedidos, D, S, CTE).
    """
    q = math.sqrt((2 * d * k) / c1)
    t = q / d
    n_pedidos = math.ceil(duracion_temporada / t)
    D = d * duracion_temporada
    S = q + Sp
    CTE = (D * k / q) + (q * c1 / 2) + (D * b) + (Sp * c1)
    return q, t, n_pedidos, D, S, CTE

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
        Resultados del procesamiento del insumo en dos listas.
    """
    b = parametros['b']
    c1 = parametros['c1']
    Sp = parametros['Sp']
    volumen_unitario = parametros['volumen_unitario']
    q, t, n_pedidos, D, S, CTE = calcular_variables(demanda, k, c1, b, Sp, duracion_temporada)
    volumen_total = S * volumen_unitario
    monto_total = S * b
    return [insumo, round(q, 2), round(t, 2), n_pedidos, round(D, 2), round(S, 2), round(CTE, 2), round(volumen_total, 2), round(monto_total, 2)], {
        "b": b,
        "D": D,
        "c1": c1,
        "k": k,
        "Sp": Sp,
        "v": volumen_unitario,
        "volumen_total": volumen_total,
        "monto_total": monto_total,
    }

def exceso_restriccion(nombre_temporada, datos_insumos, max_monto, max_volumen_sin, max_volumen_ref, carpeta):
    """
    Informa que hay restricciones que no se cumplen y genera un archivo .txt para copiar y pegar en LINGO.

    Args:
        nombre_temporada (str): Nombre de la temporada.
        datos_insumos (list): Lista de diccionarios con los datos de cada insumo necesarios para el cálculo.
        max_monto (float): Monto máximo permitido.
        max_volumen_sin (float): Volumen máximo sin refrigerar permitido.
        max_volumen_ref (float): Volumen máximo refrigerado permitido.
        carpeta (str): Carpeta donde guardar el archivo de texto.
    """
    print(f"Exceso de restricciones en la temporada {nombre_temporada}. Generando el código para LINGO...")

    # Construir el contenido del archivo
    contenido = ""
    for datos in datos_insumos:
        insumo = datos["insumo"].lower()[0]
        contenido += f"D{insumo} = {datos['D']:.2f}; c1{insumo} = {datos['c1']:.2f}; Sp{insumo} = {datos['Sp']}; "
        contenido += f"v_{insumo} = {datos['v']:.5f}; b_{insumo} = {datos['b']:.2f};\n"

    contenido += f"\nmax_monto = {max_monto};\n"
    contenido += f"max_volumen_ref = {max_volumen_ref};\n"
    contenido += f"max_volumen_sin = {max_volumen_sin};\n"

    # Crear archivo de texto
    archivo_txt = os.path.join(carpeta, f"parametros_LINGO_{nombre_temporada}.txt")
    with open(archivo_txt, mode="w", encoding="utf-8") as archivo:
        archivo.write(contenido)

    print(f"Archivo generado: {archivo_txt}")

def modelo_temporada(temporada, insumos, k, carpeta):
    """
    Implementa el modelo para todos los insumos durante una temporada, verificando el cumplimiento de restricciones.

    Args:
        temporada (dict): Información de la temporada.
        insumos (dict): Datos de los insumos.
        k (float): Costo por orden ($).
        carpeta (str): Carpeta donde se guardan los resultados.
    """
    nombre_temporada = temporada['nombre']
    duracion_temporada = temporada['duracion_temporada']
    demandas = temporada['demandas']
    
    volumen_sin_refrigerar = 0
    volumen_refrigerado = 0
    monto_total_inmovilizado = 0

    datos_insumos = []

    archivo_csv = os.path.join(carpeta, f"temporada_{nombre_temporada}.csv")
    with open(archivo_csv, mode='w', newline='', encoding='utf-8') as archivo:
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerow(["Insumo", "q (kg)", "t (sem)", "n", "D", "S_max", "CTE", "Volumen ocupado (m³)", "Monto total inmovilizado ($)"])
        
        for insumo, parametros in insumos.items():
            demanda = demandas.get(insumo, 0)
            resultados, datos_insumo = modelo_insumo(insumo, parametros, demanda, duracion_temporada, k)
            
            volumen_total = resultados[-2]
            monto_total = resultados[-1]

            if insumo.lower() == "manteca":
                volumen_refrigerado += volumen_total
            else:
                volumen_sin_refrigerar += volumen_total

            monto_total_inmovilizado += monto_total
            datos_insumo["insumo"] = insumo
            datos_insumos.append(datos_insumo)

            escritor_csv.writerow(resultados)

    if (volumen_sin_refrigerar > MAX_SIN_REFRIGERAR or 
    volumen_refrigerado > MAX_REFRIGERADO or 
    monto_total_inmovilizado > MAX_MONTO):
        exceso_restriccion(
            nombre_temporada,
            datos_insumos,
            MAX_MONTO,
            MAX_SIN_REFRIGERAR,
            MAX_REFRIGERADO,
            carpeta
        )

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
    "Harina de Trigo": {"b": 1600, "c1": 685.12, "Sp": 120, "volumen_unitario": 0.0018},
    "Azúcar": {"b": 1600, "c1": 685.12, "Sp": 4, "volumen_unitario": 0.0014},
    "Sal": {"b": 1600, "c1": 685.12, "Sp": 3, "volumen_unitario": 0.00075},
    "Manteca": {"b": 13000, "c1": 5566.6, "Sp": 12, "volumen_unitario": 0.0015}
}

# Parámetros por temporada
temporadas = [
    {"nombre": "1", "duracion_temporada": 14, "demandas": {"Harina de Trigo": 179.656, "Azúcar": 3.245, "Sal": 4.160, "Manteca": 19.907}},
    {"nombre": "2", "duracion_temporada": 20, "demandas": {"Harina de Trigo": 319.834, "Azúcar": 6.052, "Sal": 7.405, "Manteca": 22.662}},
    {"nombre": "3", "duracion_temporada": 7, "demandas": {"Harina de Trigo": 617.404, "Azúcar": 12.547, "Sal": 14.213, "Manteca": 44.75}},
    {"nombre": "4", "duracion_temporada": 11, "demandas": {"Harina de Trigo": 284.965, "Azúcar": 5.289, "Sal": 6.558, "Manteca": 22.052}}
]

# Otros parámetros constantes
k = 30000
MAX_SIN_REFRIGERAR = 24
MAX_REFRIGERADO = 3
MAX_MONTO = 3000000

# Ejecutar modelo
modelo_inventario(insumos, k, temporadas)
