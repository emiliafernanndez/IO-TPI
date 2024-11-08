# sales_cleaner.py

import pandas as pd
import re
import os

def clean_sales_data(input_file, output_file):
    # Verificar si el archivo ya existe
    if os.path.exists(output_file):
        return pd.read_csv(output_file)
    
    # Procesar datos
    data = pd.read_csv(input_file, encoding='ISO-8859-1')
    data['unit_price'] = data['unit_price'].apply(lambda x: re.sub(r'[^\d,.-]', '', x))
    data['unit_price'] = data['unit_price'].str.replace(',', '.').astype(float)
    data['Quantity'] = pd.to_numeric(data['Quantity'], errors='coerce')
    
    # Filtrar filas
    data = data[(data['Quantity'] > 0) & (data['unit_price'] > 0)]
    
    # Guardar datos limpios
    data.to_csv(output_file, index=False)
    return data
