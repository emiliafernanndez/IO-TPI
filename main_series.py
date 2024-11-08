from sales_time_series import load_and_prepare_data, create_daily_time_series, save_time_series_plots, save_class_a_products, load_class_a_products

# Rutas de archivos
input_file = 'Bakery sales.csv'
class_a_file = 'class_a_products.txt'
output_dir = 'time_series_plots'  # Carpeta donde se guardarán los gráficos

# Cargar y preparar los datos
data = load_and_prepare_data(input_file)

# Obtener los productos de clase A si es necesario
class_a_products = load_class_a_products(class_a_file)
if not class_a_products:
    class_a_products = save_class_a_products(data, class_a_file)

# Filtrar los datos solo para los productos de clase A
data_class_a = data[data['article'].isin(class_a_products)]

# Crear las series de tiempo diarias
time_series = create_daily_time_series(data_class_a)

# Guardar los gráficos de las series de tiempo en archivos
save_time_series_plots(time_series, output_dir)
