from ingredient_cleaner import clean_ingredient_data
from ingredients_abc import calculate_total_ingredients, abc_analysis_ingredients

# Ruta del archivo de ingredientes original
input_file = 'Ingredientes.csv'

# Ruta del archivo de salida limpio
output_file = 'cleaned_ingredient_data.csv'

# Limpiar y guardar los datos
clean_ingredient_data(input_file, output_file)

# Ruta del archivo de ventas (para calcular insumos necesarios)
sales_file='clean_sales_data.csv'

# Calcular Ingredientes totales
calculate_total_ingredients(sales_file, output_file)

# Ruta del archivo de Insumos Totales
insumos_totales='total_ingredients.csv'

# Ruta del análisis ABC
ingredients_abc='ingredients_abc.csv'

# Análisis ABC
abc_analysis_ingredients(insumos_totales,ingredients_abc)