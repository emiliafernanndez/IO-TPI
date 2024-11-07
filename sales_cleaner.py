import pandas as pd
import re

data = pd.read_csv('Bakery sales.csv', encoding='ISO-8859-1') # cargar Datos

# Procesar Datos
data['unit_price'] = data['unit_price'].apply(lambda x: re.sub(r'[^\d,.-]', '', x)) # elimina cualquier carácter no numérico
data['unit_price'] = data['unit_price'].str.replace(',', '.').astype(float) # formato numérico decimal
data['Quantity'] = pd.to_numeric(data['Quantity'], errors='coerce') # asegurar que 'Quantity' es numérico

# Filtrar las filas donde la cantidad y el precio unitario sean mayores que cero
data = data[data['Quantity'] > 0]
data = data[data['unit_price'] > 0]

data.to_csv('clean_sales_data.csv', index=False)