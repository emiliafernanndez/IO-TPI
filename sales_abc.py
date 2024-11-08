# sales_abc.py

import pandas as pd
import os

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
