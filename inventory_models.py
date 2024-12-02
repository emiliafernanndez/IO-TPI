import math
import csv
import os

def modelo_inventario(insumos, k, LT, temporadas):
    # Crear la carpeta 'inventory_plan' si no existe
    if not os.path.exists('inventory_plan'):
        os.makedirs('inventory_plan')

    for temporada in temporadas:
        nombre_temporada = temporada['nombre']
        duracion_temporada = temporada['duracion_temporada']
        demandas = temporada['demandas']
        
        # Definir el nombre del archivo CSV dentro de la carpeta 'inventory_plan'
        archivo_csv = f"inventory_plan/temporada_{nombre_temporada}.csv"

        with open(archivo_csv, mode='w', newline='', encoding='utf-8') as archivo:
            escritor_csv = csv.writer(archivo)
            
            # Escribir encabezados del archivo CSV
            encabezados = [
                "Insumo", "q", "t", 
                "n_pedidos", "kg", 
                "S", "CTE", "Volumen ocupado (m³)", 
                "Monto total inmovilizado ($)"
            ]
            escritor_csv.writerow(encabezados)
            
            for insumo, parametros in insumos.items():
                d = demandas[insumo]  # Demanda específica para esta temporada
                b = parametros['b']
                c1 = parametros['c1']
                Sp = parametros['Sp']
                volumen_unitario = parametros['volumen_unitario']
                volumen_maximo = parametros['volumen_maximo']
                monto_maximo = parametros['monto_maximo']
                
                # Calcular tamaño inicial del lote
                q = math.sqrt((2 * d * k) / c1)
                
                # Validar y recalcular en caso de restricciones no cumplidas
                while True:
                    # Calcular stock máximo
                    S = q + Sp
                    
                    # Validar restricciones
                    volumen_total = S * volumen_unitario
                    monto_total = S * b
                    
                    restriccion_volumen = volumen_total <= volumen_maximo
                    restriccion_monto = monto_total <= monto_maximo
                    
                    if restriccion_volumen and restriccion_monto:
                        break  # Si ambas restricciones se cumplen, continuar
                    
                    # Ajustar q si alguna restricción no se cumple
                    if not restriccion_volumen:
                        q = (volumen_maximo / volumen_unitario) - Sp
                    elif not restriccion_monto:
                        q = (monto_maximo / b) - Sp
                
                # Calcular intervalo entre reaprovisionamientos
                t = q / d
                
                # Calcular número de pedidos dentro de la temporada
                n_temporada = duracion_temporada / t
                n_pedidos = math.ceil(n_temporada)  # Redondear hacia arriba para cubrir toda la temporada
                
                # Calcular demanda total de la temporada
                D = d * duracion_temporada
                
                # Calcular costo total esperado ajustado a la temporada
                CTE = (D * k / q) + (q * c1 / 2) + (b * D) + (Sp * c1)
                
                # Escribir resultados en el archivo CSV
                escritor_csv.writerow([
                    insumo, round(q, 2), round(t, 2), n_pedidos, round(D, 2), 
                    round(S, 2), round(CTE, 2), round(volumen_total, 2), 
                    round(monto_total, 2)
                ])

# Parámetros para los insumos
insumos = {
    "Harina": {"b": 1600, "c1": 685.12, "Sp": 120, "volumen_unitario": 0.0018, "volumen_maximo": 22, "monto_maximo": 2000000},
    "Azúcar": {"b": 1600, "c1": 685.12, "Sp": 4, "volumen_unitario": 0.0014, "volumen_maximo": 1.5, "monto_maximo": 90000},
    "Sal": {"b": 1600, "c1": 685.12, "Sp": 3, "volumen_unitario": 0.00075, "volumen_maximo": 1, "monto_maximo": 110000},
    "Manteca": {"b": 13000, "c1": 5566.6, "Sp": 12, "volumen_unitario": 0.0015, "volumen_maximo": 2.5, "monto_maximo": 800000}
}

# Parámetros por temporada
temporadas = [
    {"nombre": "1", "duracion_temporada": 14, "demandas": {"Harina": 180, "Azúcar": 3.25, "Sal": 4.2, "Manteca": 20}},
    {"nombre": "2", "duracion_temporada": 20, "demandas": {"Harina": 320, "Azúcar": 6.1, "Sal": 7.5, "Manteca": 23}},
    {"nombre": "3", "duracion_temporada": 7, "demandas": {"Harina": 620, "Azúcar": 12.55, "Sal": 14.2, "Manteca": 45}},
    {"nombre": "4", "duracion_temporada": 11, "demandas": {"Harina": 285, "Azúcar": 5.3, "Sal": 6.6, "Manteca": 22}}
]

# Otros parámetros constantes
k = 30000  # costo por orden
LT = 1 / 52  # lead time (1 semana expresada en años)

# Calcular y guardar resultados
modelo_inventario(insumos, k, LT, temporadas)
