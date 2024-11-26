import pandas as pd
import os

def clean_ingredient_data(input_file, output_file):
    """
    Limpia los datos de ingredientes cargados desde un archivo CSV y guarda el resultado en otro archivo.

    Parámetros:
    - input_file: str, archivo CSV original con los  ingredientes
    - output_file, str: archivo CSV donde se guardan los datos limpios
    """
    # Cargar el archivo
    data = pd.read_csv(input_file, encoding='utf-8-sig')

    # Eliminar columnas vacías
    data.dropna(axis=1, how='all', inplace=True)

    # Renombrar columnas con los nombres de los productos
    nuevos_nombres = [
        "TRADITIONAL BAGUETTE", "FORMULE SANDWICH", "CROISSANT", "PAIN AU CHOCOLAT", "BANETTE",
        "BAGUETTE", "SANDWICH COMPLET", "SPECIAL BREAD TRAITEUR", "GRAND FAR BRETON", "TARTELETTE",
        "CEREAL BAGUETTE", "VIK BREAD", "BRIOCHE", "GD KOUIGN AMANN", "CAMPAGNE", "BOULE 400G",
        "ECLAIR", "MOISSON", "SAND JB EMMENTAL", "COMPLET", "KOUIGN AMANN", "PAIN BANETTE",
        "DIVERS VIENNOISERIE", "FINANCIER X5"
    ]
    data.columns = [data.columns[0]] + nuevos_nombres

    # Establecer la primera columna como índice antes de transponer
    data.set_index(data.columns[0], inplace=True)

    # Transponer el DataFrame para facilitar cálculos posteriores
    data = data.T

    # Rellenar valores nulos con 0
    data.fillna(0, inplace=True)

    # Guardar el DataFrame limpio en un archivo CSV
    data.to_csv(output_file)
    print(f"Datos limpiados guardados en '{output_file}'")

def abc_analysis_ingredients(file_path, output_path):
    """
    Realiza un análisis ABC de los insumos requeridos en base a un archivo con datos de ingredientes totales.

    Parámetros:
    - file_path: str, archivo CSV con los datos de ingredientes totales
    - output_path: str, archivo donde se guarda el resultado del análisis ABC

    Devuelve:
    - pd.DataFrame con los ingredientes clasificados en categorías A, B y C.
    """
    # Cargar datos de insumos totales
    data = pd.read_csv(file_path, index_col=0)

    # Calcular el total utilizado de cada insumo
    data['Total_Quantity'] = data.sum(axis=1)

    # Ordenar insumos por cantidad total en orden descendente
    data_sorted = data[['Total_Quantity']].sort_values(by='Total_Quantity', ascending=False)

    # Calcular porcentaje acumulado
    total_sum = data_sorted['Total_Quantity'].sum()
    data_sorted['Cumulative_Percentage'] = data_sorted['Total_Quantity'].cumsum() / total_sum * 100

    # Clasificar ingredientes en categorías ABC
    data_sorted['Category'] = pd.cut(data_sorted['Cumulative_Percentage'], bins=[0, 80, 95, 100], labels=['A', 'B', 'C'])

    # Guardar el análisis ABC en un archivo CSV
    data_sorted.to_csv(output_path)
    print(f"Análisis ABC guardado en '{output_path}'")

    return data_sorted

def calculate_total_ingredients(sales_file, ingredients_file, output_file):
    """
    Calcula la cantidad total de ingredientes necesarios basado en las ventas de productos de clase A.

    Parámetros:
    - sales_file: str, archivo CSV con datos de ventas.
    - ingredients_file: str, archivo CSV con datos de ingredientes.
    - output_file: str, archivo CSV donde se guarda el resultado.

    Devuelve:
    - Un archivo CSV con los ingredientes requeridos.
    """
    # Cargar datos de ventas y de ingredientes
    sales_data = pd.read_csv(sales_file)
    ingredients_data = pd.read_csv(ingredients_file, index_col=0)

    # Filtrar productos de clase A basados en los ingredientes
    class_a_products = ingredients_data.index  # Los productos de clase A están en el índice de ingredientes
    filtered_sales = sales_data[sales_data['article'].isin(class_a_products)]

    # Agrupar y sumar la cantidad total vendida de cada producto de clase A
    total_sales = filtered_sales.groupby('article')['Quantity'].sum()

    # Calcular el total de ingredientes necesarios
    total_ingredients = ingredients_data.mul(total_sales, axis=0).sum()

    # Guardar el resultado en un archivo CSV
    total_ingredients.to_csv(output_file, header=["Required Amount"])
    print(f"Archivo '{output_file}' generado con el total de ingredientes necesarios.")

# Ruta de archivos y ejecución del flujo
input_file = 'Ingredientes.csv'  # Archivo de ingredientes original
output_file = 'cleaned_ingredient_data.csv'  # Archivo de ingredientes limpios
sales_file = 'clean_sales_data.csv'  # Archivo de ventas limpias
insumos_totales = 'total_ingredients.csv'  # Archivo con insumos totales
ingredients_abc = 'ingredients_abc.csv'  # Archivo del análisis ABC

# Limpieza de ingredientes
clean_ingredient_data(input_file, output_file)

# Cálculo de ingredientes totales
calculate_total_ingredients(sales_file, output_file, insumos_totales)

# Análisis ABC de ingredientes
abc_analysis_ingredients(insumos_totales, ingredients_abc)
