import os
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_and_clean_data


def load_and_prepare_data(input_file):
    """
    Carga y prepara los datos de ventas desde un archivo CSV, calculando la demanda medida.

    Parámetros:
    - input_file: str, archivo CSV con los datos de ventas.

    Devuelve:
    - pd.DataFrame, datos preparados con una columna de demanda medida.
    """
    # Cargar y limpiar los datos
    data = load_and_clean_data(input_file)
    # Calcular la demanda medida
    data['MeasuredDemand'] = data['Quantity'] * data['unit_price']
    return data


def create_time_series(data, freq='D'):
    """
    Crea las series de tiempo para cada producto según la frecuencia especificada.

    Parámetros:
    - data: pd.DataFrame, datos de ventas con 'MeasuredDemand'.
    - freq: str, frecuencia de agrupamiento (por defecto es diaria, es decir, 'D')

    Devuelve:
    - pd.DataFrame con las series de tiempo de cada producto.
    """
    # Agrupar por artículo y fecha, sumando la demanda medida
    data_grouped = data.groupby(['article', pd.Grouper(key='date', freq=freq)])['MeasuredDemand'].sum().reset_index()

    # Crear el rango de fechas completo
    min_date = data_grouped['date'].min()
    max_date = data_grouped['date'].max()
    all_days = pd.date_range(min_date, max_date, freq=freq)

    # Crear un DataFrame para todas las series temporales
    time_series_df = pd.DataFrame({'date': all_days})

    # Agregar las series temporales de cada producto
    for producto in data_grouped['article'].unique():
        
        # Filtrar y ajustar las fechas de cada producto
        producto_data = data_grouped[data_grouped['article'] == producto]
        producto_data = producto_data.set_index('date').reindex(all_days, fill_value=0).reset_index()
        producto_data.rename(columns={'index': 'date', 'MeasuredDemand': producto}, inplace=True)

        # Unir los datos del producto con el DataFrame general
        time_series_df = time_series_df.merge(producto_data[['date', producto]], on='date', how='left')

    return time_series_df


def save_time_series_to_csv(time_series_df, output_file):
    """
    Guarda las series de tiempo en un archivo CSV.

    Parámetros:
    - time_series_df: pd.DataFrame, DataFrame con las series de tiempo de los productos.
    - output_file: str, ruta donde se guarda el archivo CSV con las series de tiempo.
    """
    time_series_df.to_csv(output_file, index=False)
    print(f"Series temporales guardadas en {output_file}")


def save_time_series_plots(time_series_df, output_dir):
    """
    Crea y guarda gráficos de las series de tiempo de cada producto en un directorio.

    Parámetros:
    - time_series_df: pd.DataFrame, DataFrame con las series de tiempo de los productos.
    - output_dir: str, ruta del directorio donde se guardarán los gráficos.
    """
    # Crear el directorio si no existe
    os.makedirs(output_dir, exist_ok=True)

    # Crear y guardar gráficos para cada producto
    for producto in time_series_df.columns[1:]:  # Ignorar la columna 'date'
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(time_series_df['date'], time_series_df[producto], marker='o')
        ax.set_title(f'Serie de Tiempo para {producto}')
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Demanda Medida')

        # Guardar cada gráfico como imagen
        output_file = os.path.join(output_dir, f'{producto}_time_series.png')
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close(fig)  # Cerrar la figura para liberar memoria


def load_class_a_products(output_file):
    """
    Carga los productos de clase A desde un archivo de texto.

    Parámetros:
    - output_file: str, archivo de texto que contiene los productos de clase A.

    Devuelve:
    - list, lista de productos de clase A.

    Lanza:
    - FileNotFoundError si el archivo no existe.
    """
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            return f.read().splitlines()
    raise FileNotFoundError(f"El archivo {output_file} no existe. Recordá generar los productos de clase A previamente.")


# Rutas de archivos
input_file = 'Bakery sales.csv'  # Dataset original
class_a_file = 'class_a_products.txt'  # Archivo con productos de clase A
output_dir_base = 'products_time_series'  # Carpeta base para gráficos
csv_output_file = 'products_time_series.csv'  # Archivo CSV de series de tiempo

# Elegir la frecuencia (puede ser 'D', 'W', o 'M')
freq = 'W'
output_dir = os.path.join(output_dir_base, freq)  # Crear subcarpeta para esa frecuencia

# Cargar y preparar los datos
data = load_and_prepare_data(input_file)  # Datos de ventas
class_a_products = load_class_a_products(class_a_file)  # Productos de clase A
data_class_a = data[data['article'].isin(class_a_products)]  # Filtrar datos para productos de clase A

# Crear las series de tiempo según la frecuencia elegida
time_series_df = create_time_series(data_class_a, freq=freq)

# Guardar las series temporales
save_time_series_to_csv(time_series_df, csv_output_file)  # Guardar archivo CSV
save_time_series_plots(time_series_df, output_dir)  # Guardar gráficos
