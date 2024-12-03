import pandas as pd
import matplotlib.pyplot as plt
from utils import crear_carpeta
import os

def plot_weekly_ingredient_series(ingredient_series_data, output_folder):
    """
    Genera gráficos de series de tiempo semanales para cada insumo y los guarda en una carpeta.

    Parámetros:
    - ingredient_series_data: str, archivo CSV con los datos semanales de insumos.
    - output_folder: str, carpeta donde se guardarán los gráficos generados.
    """
    # Cargar datos semanales de insumos desde un archivo CSV
    weekly_ingredients = pd.read_csv(ingredient_series_data, index_col=0, parse_dates=True, encoding='utf-8-sig')
    
    # Crear la carpeta de salida si no existe
    crear_carpeta(output_folder)

    # Generar gráficos para cada columna (insumo) en el archivo
    for ingredient in weekly_ingredients.columns:
        plt.figure(figsize=(10, 6))
        plt.plot(weekly_ingredients.index, weekly_ingredients[ingredient], marker='o', linestyle='-')
        plt.title(f'Serie de Tiempo Semanal para {ingredient}')
        plt.xlabel('Semana')
        plt.ylabel('Cantidad Usada')
        plt.grid(True)

        # Guardar el gráfico en un archivo dentro de la carpeta de salida
        file_path = os.path.join(output_folder, f'{ingredient}_weekly_series.png')
        plt.savefig(file_path)
        plt.close()  # Cerrar el gráfico para liberar memoria
        print(f'Gráfico guardado en: {file_path}')

    print(f"Gráficos generados y guardados en la carpeta '{output_folder}'.")

def generate_weekly_ingredient_series(sales_data_path, ingredient_data_path, selected_ingredients, ingredient_series_data):
    """
    Genera series de tiempo semanales para insumos seleccionados y las guarda en un archivo CSV.

    Parámetros:
    - sales_data_path: Ruta al archivo CSV con los datos de ventas.
    - ingredient_data_path: Ruta al archivo CSV con los datos de ingredientes por producto.
    - selected_ingredients: Lista de insumos a incluir en las series de tiempo.
    - ingredient_series_data: Ruta donde se guardará el archivo con las series de tiempo semanales.
    """
    # Cargar los datos de ventas y de ingredientes
    sales_data = pd.read_csv(sales_data_path, parse_dates=['date'], encoding='utf-8-sig')
    ingredient_data = pd.read_csv(ingredient_data_path, index_col=0, encoding='utf-8-sig')

    # Filtrar solo las columnas de los ingredientes seleccionados
    ingredient_data = ingredient_data[selected_ingredients]

    # Crear una columna de semana en el dataset de ventas para agrupar
    sales_data['week'] = sales_data['date'].dt.to_period('W').dt.start_time

    # Inicializar un DataFrame vacío con semanas como índice y los insumos seleccionados como columnas
    weekly_ingredients = pd.DataFrame(index=sales_data['week'].unique(), columns=selected_ingredients).fillna(0)

    # Agrupar las ventas por producto y semana para calcular los insumos usados
    for product, group in sales_data.groupby('article'):
        if product in ingredient_data.index:  # Verificar si el producto tiene ingredientes registrados
            product_ingredients = ingredient_data.loc[product]
            for week, week_data in group.groupby('week'):
                total_quantity = week_data['Quantity'].sum()  # Sumar la cantidad total vendida en la semana
                weekly_ingredients.loc[week] += total_quantity * product_ingredients  # Multiplicar por los insumos

    # Guardar el resultado en un archivo CSV
    weekly_ingredients.to_csv(ingredient_series_data)
    print(f"Series de tiempo semanales generadas y guardadas en {ingredient_series_data}")

# Definición de rutas de archivos y carpetas
sales_data_path = 'clean_sales_data.csv'
ingredient_data_path = 'cleaned_ingredient_data.csv'
ingredient_series_data = 'weekly_ingredients.csv'
output_folder = 'ingredient_time_series'

# Lista de ingredientes seleccionados para analizar
selected_ingredients = ['Harina de Trigo (g)', 'Manteca (g)', 'Sal (g)', 'Azúcar (g)']

# Generar las series de tiempo semanales y guardarlas en un archivo CSV
generate_weekly_ingredient_series(
    sales_data_path, 
    ingredient_data_path, 
    selected_ingredients, 
    ingredient_series_data
)

# Generar gráficos para las series de tiempo guardadas
plot_weekly_ingredient_series(
    ingredient_series_data, 
    output_folder
)
