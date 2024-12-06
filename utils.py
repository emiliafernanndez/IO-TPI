import pandas as pd
import re
import os

def load_and_clean_data(input_file):
    """
    Carga y limpia los datos de ventas del dataset original.
    
    Args:
        input_file (str): Ruta del archivo CSV de entrada.
    
    Returns:
        pd.DataFrame: DataFrame limpio y procesado.

    """
    data = pd.read_csv(input_file, encoding='ISO-8859-1')
    
    # Eliminar todo símbolo no numérico del precio unitario.
    data['unit_price'] = data['unit_price'].apply(lambda x: re.sub(r'[^\d,.-]', '', x))
    
    # Convertir a formato numérico el precio unitario y la cantidad.
    data['unit_price'] = data['unit_price'].str.replace(',', '.').astype(float) # también cambia separador decimal
    data['Quantity'] = pd.to_numeric(data['Quantity'], errors='coerce')
    
    # Convertir la fecha a un formato apropiado.
    data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
    
    # Filtrar filas con cantidades o precios negativos
    data = data[(data['Quantity'] > 0) & (data['unit_price'] > 0)]
    
    return data

def crear_carpeta(carpeta):
    """
    Crea una carpeta si no existe.

    Args:
        carpeta (str): Ruta de la carpeta a crear.
    """
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)