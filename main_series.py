from sales_time_series import load_and_prepare_data, create_time_series, save_time_series_plots, save_class_a_products, load_class_a_products
import os

# Rutas de archivos
input_file = 'Bakery sales.csv'
class_a_file = 'class_a_products.txt'
output_dir_base = 'time_series_plots'  # Carpeta base para guardar los gráficos

# Elegir la frecuencia (puede ser 'D', 'W', o 'M')
freq = 'M'  # 'D' para diario, 'W' para semanal, 'M' para mensual

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
