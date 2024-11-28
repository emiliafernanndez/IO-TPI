import math

def modelo_inventario (insumos, k, Sp, LT):
    resultados = {}
    for insumo, parametros in insumos.items():
        D = parametros['D']
        b = parametros['b']
        c1 = parametros['c1']
        
        # Calcular tamaño del lote
        q = math.sqrt((2 * D * k) / c1)
        
        # Calcular intervalo entre reaprovisionamientos
        t = q / D
        
        # Calcular stock de reorden
        SR = D * LT + Sp
        
        # Calcular stock máximo
        S = q + Sp
        
        # Calcular costo total esperado
        CTE = (D * k / q) + (q * c1 / 2) + (b * D) + (Sp * c1)
        
        # Guardar resultados para este insumo
        resultados[insumo] = {
            "Tamaño del lote (q)": q,
            "Intervalo entre reaprovisionamientos (t)": t,
            "Stock de reorden (SR)": SR,
            "Stock máximo (S)": S,
            "Costo total esperado (CTE)": CTE
        }
    return resultados

# Parámetros para los insumos
insumos = {
    "Harina": {"D": 1200, "b": 1600, "c1": 685.12},
    "Azúcar": {"D": 800, "b": 1600, "c1": 685.12},
    "Sal": {"D": 500, "b": 13000, "c1": 685.12},
    "Manteca": {"D": 600, "b": 1600, "c1": 5566.6}
}

# Otros parámetros constantes
k = 30000   # costo por orden
Sp = 50     # stock de protección
LT = 1 / 52 # lead time (1 semana expresada en años)

# Calcular resultados
resultados = modelo_inventario (insumos, k, Sp, LT)

# Imprimir resultados
for insumo, valores in resultados.items():
    print(f"\nResultados para {insumo}:")
    for key, value in valores.items():
        print(f"  {key}: {value:.2f}")
