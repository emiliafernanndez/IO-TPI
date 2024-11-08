import os
from sales_cleaner import clean_sales_data
from sales_abc import abc_analysis, save_class_a_products, load_class_a_products

# Nombres de archivo
input_file = 'Bakery sales.csv'
cleaned_file = 'clean_sales_data.csv'
abc_result_file = 'abc_analysis_result.csv'
class_a_file = 'class_a_products.txt'

# LIMPIEZA DE DATOS
cleaned_data = clean_sales_data(input_file, cleaned_file)

# ANÁLISIS ABC
abc_result = abc_analysis(cleaned_data, abc_result_file)

# OBTENER PRODUCTOS DE CLASE A
class_a_products = load_class_a_products(class_a_file)
if not class_a_products:
    class_a_products = save_class_a_products(abc_result, class_a_file)

# Mostrar productos de clase A
print("Productos de clase A:", class_a_products)
