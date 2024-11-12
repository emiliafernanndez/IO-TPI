import pandas as pd

def abc_analysis_ingredients(file_path, output_path):
    """
    Realiza un análisis ABC de los insumos requeridos en base al archivo total_ingredients.csv.
    
    Parámetros:
        - file_path: Ruta al archivo CSV con los datos de ingredientes totales.
        - output_path: Ruta donde se guardará el resultado del análisis ABC de ingredientes.
    
    Retorna:
        Un DataFrame con los ingredientes clasificados en categorías A, B y C.
    """
    # Cargar datos de ingredientes totales
    data = pd.read_csv(file_path, index_col=0)
    
    # Calcular la cantidad total utilizada de cada insumo
    data['Total_Quantity'] = data.sum(axis=1)
    
    # Ordenar insumos por cantidad total en orden descendente
    data_sorted = data[['Total_Quantity']].sort_values(by='Total_Quantity', ascending=False)
    
    # Calcular el porcentaje acumulado de cada insumo
    total_sum = data_sorted['Total_Quantity'].sum()
    data_sorted['Cumulative_Percentage'] = data_sorted['Total_Quantity'].cumsum() / total_sum * 100
    
    # Asignar categorías ABC
     # Asignar categorías ABC usando pd.cut
    data_sorted['Category'] = pd.cut(data_sorted['Cumulative_Percentage'], bins=[0, 80, 95, 100], labels=['A', 'B', 'C'])
    
    
    
    #data_sorted['Category'] = 'C'
    #data_sorted.loc[data_sorted['Cumulative_Percentage'] <= 80, 'Category'] = 'A'
    #data_sorted.loc[(data_sorted['Cumulative_Percentage'] > 80) & (data_sorted['Cumulative_Percentage'] <= 95), 'Category'] = 'B'
    
    # Guardar el resultado en un archivo CSV
    data_sorted.to_csv(output_path)
    
    return data_sorted

def calculate_total_ingredients(sales_file: str, ingredients_file: str, output_file: str = 'total_ingredients.csv'):
    # Cargar el archivo de ventas y de ingredientes
    sales_data = pd.read_csv(sales_file)
    ingredients_data = pd.read_csv(ingredients_file, index_col=0)

    # Filtrar los productos de clase A en las ventas
    class_a_products = ingredients_data.index  # Usamos el índice de ingredientes como la lista de productos de clase A
    filtered_sales = sales_data[sales_data['article'].isin(class_a_products)]

    # Agrupar y sumar la cantidad total vendida de cada producto de clase A
    total_sales = filtered_sales.groupby('article')['Quantity'].sum()

    # Calcular el total de ingredientes necesarios
    total_ingredients = ingredients_data.mul(total_sales, axis=0).sum()

    # Guardar el resultado en un archivo CSV
    total_ingredients.to_csv(output_file, header=["Required Amount"])

    print(f"Archivo '{output_file}' generado con el total de ingredientes necesarios.")