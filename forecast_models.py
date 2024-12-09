import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
import warnings
from sklearn.metrics import mean_absolute_error, mean_squared_error
from utils import crear_carpeta

warnings.filterwarnings("ignore")

def load_data(filepath):
    # Cargar los datos de la serie de tiempo
    data = pd.read_csv(filepath, index_col=0, parse_dates=True, encoding='utf-8-sig')
    return data

def check_stationarity(series):
    # Realizar la prueba de Dickey-Fuller para verificar la estacionaridad
    result = adfuller(series.dropna())
    return result[1] <= 0.05  # Retorna True si es estacionaria

def difference_series(series):
    # Diferenciar la serie si no es estacionaria
    return series.diff().dropna()

def fit_sarima_model(series, order=(1,1,1), seasonal_order=(1,1,1,52)):
    # Ajustar el modelo SARIMA
    model = SARIMAX(series, order=order, seasonal_order=seasonal_order, enforce_stationarity=False, enforce_invertibility=False)
    result = model.fit(disp=False)
    return result

def generate_forecasts(result, steps=48, repetitions=100):
    # Generar múltiples pronósticos para reflejar la variabilidad
    forecasts = []

    for _ in range(repetitions):
        forecast = result.get_forecast(steps=steps).predicted_mean.clip(lower=0)  # Evita valores negativos
        forecasts.append(forecast)

    forecasts_df = pd.DataFrame(forecasts).T
    forecasts_df.index = pd.date_range(result.data.dates[-1] + pd.Timedelta(weeks=1), periods=steps, freq='W')
    
    # Pronóstico promedio de todas las simulaciones
    forecast_series = forecasts_df.mean(axis=1)
    
    return forecast_series, forecasts_df

def save_forecast_plots(series, forecast, ingredient_name, output_folder='ingredients_forecast'):
    """
    Guarda gráficos de pronóstico para un insumo específico.

    Parámetros:
    - series: serie de datos históricos.
    - forecast: serie de pronóstico.
    - ingredient_name: nombre del insumo.
    - output_folder: carpeta donde van los gráficos.
    """
    # Crear la carpeta de salida si no existe
    crear_carpeta(output_folder)
    
    # Graficar la serie original y el pronóstico
    plt.figure(figsize=(10, 6))
    plt.plot(series, label='Datos Históricos', color='black', marker='o')
    plt.plot(forecast, label='Pronóstico', color='green', linestyle='--', marker='o')

    # Agregar títulos y etiquetas
    plt.title(f'Pronóstico Semanal para {ingredient_name}', fontsize=14, fontweight='normal', loc='center')
    plt.xlabel('Fecha')
    plt.ylabel('Cantidad Usada')
    plt.legend()
    plt.grid(True)
    
    # Guardar el gráfico en la carpeta especificada
    file_path = os.path.join(output_folder, f'{ingredient_name}_forecast.png')
    plt.savefig(file_path)
    plt.close()
    print(f'Gráfico de pronóstico guardado en: {file_path}')

def save_forecasts_to_csv(forecasts, output_path='ingredient_forecasts.csv'):
    """
    Guarda los pronósticos en un único archivo CSV.
    
    Parámetros:
    - forecasts: diccionario donde las claves son nombres de insumos y los valores son series de pronósticos.
    - output_path: ruta del archivo CSV de salida.
    """
    # Combinar los pronósticos en un DataFrame
    forecast_df = pd.concat(forecasts, axis=1)
    forecast_df.columns = forecasts.keys()
    
    # Guardar en CSV
    forecast_df.to_csv(output_path, encoding='utf-8-sig')
    print(f'Pronósticos guardados en: {output_path}')

# Cargar el archivo de datos de ejemplo
filepaths = ['weekly_ingredients.csv']  # Ajusta el nombre del archivo según corresponda
forecast_results = {}  # Diccionario para almacenar los pronósticos de cada insumo

for filepath in filepaths:
    data = load_data(filepath)
    for column in data.columns:
        print(f"\nPronóstico para {column}")
        series = data[column]
        
        # Verificar si la serie es estacionaria
        if not check_stationarity(series):
            print("La serie no es estacionaria, aplicando diferenciación.")
            series = difference_series(series)
        else:
            print("La serie es estacionaria.")
        
        # Ajustar el modelo SARIMA
        sarima_result = fit_sarima_model(series)
        
        # Generar pronósticos para las siguientes 48 semanas
        forecast, simulations_df = generate_forecasts(sarima_result, steps=48, repetitions=100)
        
        # Guardar el gráfico de pronóstico
        save_forecast_plots(data[column], forecast, column)
        
        # Guardar el pronóstico en el diccionario
        forecast_results[column] = forecast

# Guardar todos los pronósticos en un único archivo CSV
save_forecasts_to_csv(forecast_results)
