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

    # Crear series de tiempo para cada artículo, asegurándose de que cada período esté representado
    time_series = {}
    for producto in data_grouped['article'].unique():
        # Filtrar datos para el producto actual
        producto_data = data_grouped[data_grouped['article'] == producto]

        # Reindexar para incluir todos los períodos, incluso los sin ventas (se llena con 0)
        producto_data = producto_data.set_index('date').reindex(all_days, fill_value=0).reset_index()
        producto_data.rename(columns={'index': 'date'}, inplace=True)

        # Almacenar la serie de tiempo para el producto
        time_series[producto] = producto_data
    
    return time_series

def save_time_series_plots(time_series, output_dir):
    # Asegurarse de que el directorio de salida exista
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Graficar las series de tiempo de cada producto y guardarlas como archivos
    for producto, producto_data in time_series.items():
        fig, ax = plt.subplots(figsize=(10, 5))  # crear un gráfico por producto
        ax.plot(producto_data['date'], producto_data['MeasuredDemand'], marker='o')
        ax.set_title(f'Serie de Tiempo para {producto}')
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Demanda Medida')

        # Guardar el gráfico en un archivo
        output_file = os.path.join(output_dir, f'{producto}_time_series.png')
        plt.tight_layout()
        plt.savefig(output_file)  # Guardar el gráfico como imagen
        plt.close(fig)  # Cerrar la figura para liberar memoria

def save_class_a_products(data, output_file):
    # Realizar análisis ABC para obtener productos de clase A
    data['MeasuredDemand'] = data['Quantity'] * data['unit_price']
    data = data.groupby(['article'])['MeasuredDemand'].sum().reset_index()
    data['PorcentualMeasuredDemand'] = data['MeasuredDemand'] * 100 / data['MeasuredDemand'].sum()
    data = data.sort_values(by=['MeasuredDemand'], ascending=False)
    data['CumulativePercentage'] = data['PorcentualMeasuredDemand'].cumsum()
    
    percentage = [0, 80, 95, 100]
    categories = ['A', 'B', 'C']
    data['Category'] = pd.cut(data['CumulativePercentage'], bins=percentage, labels=categories)
    
    data_tipo_A = data[data['Category'] == 'A']
    productos_clase_A = data_tipo_A['article'].unique()

    # Guardar los productos de clase A en un archivo
    with open(output_file, 'w') as f:
        f.write('\n'.join(productos_clase_A))

    return productos_clase_A

def load_class_a_products(output_file):
    # Cargar productos de clase A desde el archivo
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            return f.read().splitlines()
    return []

# Rutas de archivos
input_file = 'Bakery sales.csv'
class_a_file = 'class_a_products.txt'
output_dir_base = 'products_time_series'  # Carpeta base para guardar los gráficos

# Elegir la frecuencia (puede ser 'D', 'W', o 'M')
freq = 'W'  # 'D' para diario, 'W' para semanal, 'M' para mensual

# Crear un subdirectorio para la frecuencia elegida
output_dir = os.path.join(output_dir_base, freq)

# Cargar y preparar los datos
data = load_and_prepare_data(input_file)

# Obtener los productos de clase A si es necesario
class_a_products = load_class_a_products(class_a_file)
if not class_a_products:
    class_a_products = save_class_a_products(data, class_a_file)

# Filtrar los datos solo para los productos de clase A
data_class_a = data[data['article'].isin(class_a_products)]

# Crear las series de tiempo según la frecuencia elegida
time_series = create_time_series(data_class_a, freq=freq)

# Guardar los gráficos de las series de tiempo en archivos
save_time_series_plots(time_series, output_dir)
