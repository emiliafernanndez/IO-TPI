from ingredient_cleaner import clean_ingredient_data

# Ruta del archivo de ingredientes original
input_file = 'Ingredientes.csv'

# Ruta del archivo de salida limpio
output_file = 'cleaned_ingredient_data.csv'

# Limpiar y guardar los datos
clean_ingredient_data(input_file, output_file)
