import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_weekly_ingredient_series(weekly_ingredient_path, output_folder):
    weekly_ingredients = pd.read_csv(weekly_ingredient_path, index_col=0, parse_dates=True, encoding='utf-8-sig')  # Con codificación
    os.makedirs(output_folder, exist_ok=True)

    # Graficar cada insumo individualmente
    for ingredient in weekly_ingredients.columns:
        plt.figure(figsize=(10, 6))
        plt.plot(weekly_ingredients.index, weekly_ingredients[ingredient], marker='o', linestyle='-')
        plt.title(f'Serie de Tiempo Semanal para {ingredient}')
        plt.xlabel('Semana')
        plt.ylabel('Cantidad Usada')
        plt.grid(True)

        # Guardar el gráfico en la carpeta especificada
        file_path = os.path.join(output_folder, f'{ingredient}_weekly_series.png')
        plt.savefig(file_path)
        plt.close()
        print(f'Gráfico guardado en: {file_path}')

    print("Gráficos de series de tiempo generados y guardados en la carpeta '/ingredient_time_series'.")

def generate_weekly_ingredient_series(sales_data_path, ingredient_data_path, selected_ingredients, output_path):
    # Cargar los datos de ventas y los ingredientes
    sales_data = pd.read_csv(sales_data_path, parse_dates=['date'], encoding='utf-8-sig')
    ingredient_data = pd.read_csv(ingredient_data_path, index_col=0, encoding='utf-8-sig')

    # Filtrar las columnas de ingredientes seleccionados
    ingredient_data = ingredient_data[selected_ingredients]

    # Crear una columna de semana para agrupar
    sales_data['week'] = sales_data['date'].dt.to_period('W').dt.start_time

    # Calcular el uso semanal de cada insumo
    weekly_ingredients = pd.DataFrame(index=sales_data['week'].unique(), columns=selected_ingredients).fillna(0)

    for product, group in sales_data.groupby('article'):
        if product in ingredient_data.index:
            product_ingredients = ingredient_data.loc[product]
            # Agrupar por semana y calcular la cantidad total de insumo por semana
            for week, week_data in group.groupby('week'):
                total_quantity = week_data['Quantity'].sum()
                weekly_ingredients.loc[week] += total_quantity * product_ingredients

    # Guardar el resultado
    weekly_ingredients.to_csv(output_path)

    print(f"Series de tiempo semanales generadas y guardadas en {output_path}")

selected_ingredients=['Harina de Trigo (g)','Manteca (g)','Sal (g)','Azúcar (g)']

generate_weekly_ingredient_series('clean_sales_data.csv', 'cleaned_ingredient_data.csv', selected_ingredients, 'weekly_ingredients.csv')

# Llamada a la función con el archivo de datos de ingredientes semanales
plot_weekly_ingredient_series('weekly_ingredients.csv','ingredient_time_series')
