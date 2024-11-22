import os
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_and_clean_data

def load_and_prepare_data(input_file):
    data = load_and_clean_data(input_file)
    data['MeasuredDemand'] = data['Quantity'] * data['unit_price']
    return data

def create_time_series(data, freq='D'):
    # Agrupar por artículo y frecuencia, sumando la demanda medida
    data_grouped = data.groupby(['article', pd.Grouper(key='date', freq=freq)])['MeasuredDemand'].sum().reset_index()

    # Crear el rango de fechas completo
    min_date = data_grouped['date'].min()
    max_date = data_grouped['date'].max()
    all_days = pd.date_range(min_date, max_date, freq=freq)

    # Crear series de tiempo para cada artículo
    time_series = {}
    for producto in data_grouped['article'].unique():
        # Filtrar datos para el producto actual
        producto_data = data_grouped[data_grouped['article'] == producto]

        # Reindexar para incluir todos los días, incluso los sin ventas (se llena con 0)
        producto_data = producto_data.set_index('date').reindex(all_days, fill_value=0).reset_index()
        producto_data.rename(columns={'index': 'date'}, inplace=True)

        # Almacenar la serie de tiempo para el producto
        time_series[producto] = producto_data

    return time_series

def save_time_series_plots(time_series, output_dir):
    # Asegurarse de que existe la carpeta de salida, crearla si no
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Graficar y guardar en archivos las series de tiempo de cada producto
    for producto, producto_data in time_series.items():
        fig, ax = plt.subplots(figsize=(10, 5)) 
        ax.plot(producto_data['date'], producto_data['MeasuredDemand'], marker='o')
        ax.set_title(f'Serie de Tiempo para {producto}')
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Demanda Medida')

        # Guardar cada gráfico en un archivo
        output_file = os.path.join(output_dir, f'{producto}_time_series.png')
        plt.tight_layout()
        plt.savefig(output_file)  # guardar gráfico como imagen
        plt.close(fig)  # cerrar figura para liberar memoria

def load_class_a_products(output_file):
    # Cargar productos de clase A desde el archivo
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            return f.read().splitlines()
    raise FileNotFoundError(f"El archivo {output_file} no existe. Recordá generar los productos de clase A previamente.")

# Rutas de archivos
input_file = 'Bakery sales.csv' # dataset original
class_a_file = 'class_a_products.txt' # .txt con productos de clase A
output_dir_base = 'products_time_series'  # carpeta de gráficos

# Elegir la frecuencia (puede ser 'D', 'W', o 'M')
freq = 'W' 
output_dir = os.path.join(output_dir_base, freq) # crear subcarpeta para esa frecuencia

# Cargar y preparar datos
data = load_and_prepare_data(input_file) # datos de ventas
class_a_products = load_class_a_products(class_a_file) # productos de clase A
data_class_a = data[data['article'].isin(class_a_products)] # filtrar datos para los productos de clase A

# Crear y guardar las series de tiempo según la frecuencia elegida
time_series = create_time_series(data_class_a, freq=freq)
save_time_series_plots(time_series, output_dir)