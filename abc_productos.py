import os
import pandas as pd
from utils import load_and_clean_data

def clean_sales_data(input_file, output_file):
    """
    Limpia y carga los datos de ventas desde un archivo CSV.

    Parámetros:
    - input_file: str, archivo CSV original con los datos de ventas.
    - output_file: str, archivo CSV donde se guardan los datos limpios.

    Devuelve:
    - pd.DataFrame con los datos limpios de ventas.
    """
    # Si el archivo limpio ya existe, cargamos y devolvemos el DataFrame
    if os.path.exists(output_file):
        return pd.read_csv(output_file)
    
    # Si el archivo no existe, limpiamos los datos y los guardamos
    data = load_and_clean_data(input_file)
    data.to_csv(output_file, index=False)
    return data


def abc_analysis(data, output_file):
    """
    Realiza el análisis ABC sobre los datos de ventas, clasificando los productos
    según su demanda medida.

    Parámetros:
    - data: pd.DataFrame, datos de ventas limpios.
    - output_file: str, archivo CSV  donde se guarda el resultado del análisis.

    Devuelve:
    - pd.DataFrame con el análisis ABC, incluyendo categorías A, B y C.
    """
    # Verificar si el archivo de análisis ABC ya existe
    if os.path.exists(output_file):
        return pd.read_csv(output_file)
    
    # Realizar análisis ABC: calcular la demanda medida y ordenar los productos
    data['MeasuredDemand'] = data['Quantity'] * data['unit_price']
    data = data.groupby(['article'])['MeasuredDemand'].sum().reset_index()
    data = data.sort_values(by=['MeasuredDemand'], ascending=False)
    
    # Calcular porcentajes y categorización
    data['PorcentualMeasuredDemand'] = (data['MeasuredDemand'] * 100) / data['MeasuredDemand'].sum()
    data['CumulativePercentage'] = data['PorcentualMeasuredDemand'].cumsum()
    data['Category'] = pd.cut(data['CumulativePercentage'], bins=[0, 80, 95, 100], labels=['A', 'B', 'C'])
    
    # Guardar el resultado del análisis ABC
    data.to_csv(output_file, index=False)
    return data


def save_class_a_products(data, output_file):
    """
    Guarda los productos de clase A en un archivo de texto.

    Parámetros:
    - data: pd.DataFrame, datos con el análisis ABC que incluye la categoría de los productos.
    - output_file: str, archivo de texto donde se guardan los productos de clase A.

    Devuelve:
    - list, lista de productos de clase A.
    """
    # Filtrar los productos de clase A y guardarlos en el archivo
    class_a_products = data[data['Category'] == 'A']['article'].tolist()
    with open(output_file, 'w') as f:
        f.write('\n'.join(class_a_products))
    return class_a_products


def load_class_a_products(output_file):
    """
    Carga los productos de clase A desde un archivo de texto.

    Parámetros:
    - output_file: str, archivo de texto que contiene los productos de clase A.

    Devuelve:
    - list, lista de productos de clase A, o None si el archivo no existe.
    """
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            return f.read().splitlines()
    return None


# Nombres de los archivos
input_file = 'Bakery sales.csv'
cleaned_file = 'clean_sales_data.csv'
abc_result_file = 'abc_analysis_result.csv'
class_a_file = 'class_a_products.txt'

# Limpieza de datos
cleaned_data = clean_sales_data(input_file, cleaned_file)

# Análisis ABC
abc_result = abc_analysis(cleaned_data, abc_result_file)

# Cargar los productos de clase A (o guardarlos si no existen)
class_a_products = load_class_a_products(class_a_file)
if not class_a_products:
    class_a_products = save_class_a_products(abc_result, class_a_file)

# Mostrar los productos de clase A
print("Productos de clase A:", class_a_products)