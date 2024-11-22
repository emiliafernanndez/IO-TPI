import os
import pandas as pd
from utils import load_and_clean_data

def clean_sales_data(input_file, output_file):
    if os.path.exists(output_file):
        return pd.read_csv(output_file)
    data = load_and_clean_data(input_file)
    data.to_csv(output_file, index=False)
    return data

def abc_analysis(data, output_file):
    # Verificar si el archivo de análisis ABC ya existe
    if os.path.exists(output_file):
        return pd.read_csv(output_file)
    
    # Realizar análisis ABC
    data['MeasuredDemand'] = data['Quantity'] * data['unit_price']
    data = data.groupby(['article'])['MeasuredDemand'].sum().reset_index()
    data = data.sort_values(by=['MeasuredDemand'], ascending=False)
    data['PorcentualMeasuredDemand'] = data['MeasuredDemand'] * 100 / data['MeasuredDemand'].sum()
    data['CumulativePercentage'] = data['PorcentualMeasuredDemand'].cumsum()
    data['Category'] = pd.cut(data['CumulativePercentage'], bins=[0, 80, 95, 100], labels=['A', 'B', 'C'])
    
    # Guardar resultado del análisis ABC
    data.to_csv(output_file, index=False)
    return data

def save_class_a_products(data, output_file):
    class_a_products = data[data['Category'] == 'A']['article'].tolist()
    with open(output_file, 'w') as f:
        f.write('\n'.join(class_a_products))
    return class_a_products

def load_class_a_products(output_file):
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            return f.read().splitlines()
    return None

# Nombres de archivo
input_file = 'Bakery sales.csv'
cleaned_file = 'clean_sales_data.csv'
abc_result_file = 'abc_analysis_result.csv'
class_a_file = 'class_a_products.txt'

# LIMPIEZA DE DATOS
cleaned_data = clean_sales_data(input_file, cleaned_file)

# ANÁLISIS ABC
abc_result = abc_analysis(cleaned_data, abc_result_file)

# OBTENER PRODUCTOS DE CLASE A
class_a_products = load_class_a_products(class_a_file)
if not class_a_products:
    class_a_products = save_class_a_products(abc_result, class_a_file)

# Mostrar productos de clase A
print("Productos de clase A:", class_a_products)