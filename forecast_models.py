import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
import warnings
from sklearn.metrics import mean_absolute_error, mean_squared_error

warnings.filterwarnings("ignore")

def load_data(filepath):
    # Cargar los datos de la serie de tiempo
    data = pd.read_csv(filepath, index_col=0, parse_dates=True)
    return data

def check_stationarity(series):
    # Realiza la prueba de Dickey-Fuller para verificar la estacionaridad
    result = adfuller(series.dropna())
    return result[1] <= 0.05  # Retorna True si es estacionaria

def difference_series(series):
    # Diferencia la serie si no es estacionaria
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
    # Crear la carpeta de salida si no existe
    os.makedirs(output_folder, exist_ok=True)
    
    # Graficar la serie original, el pronóstico y las simulaciones
    plt.figure(figsize=(10, 6))
    plt.plot(series, label='Datos Históricos', color='black', marker='o')
    plt.plot(forecast, label='Pronóstico', color='green', linestyle='--', marker='o')

    plt.xlabel('Fecha')
    plt.ylabel('Cantidad Usada')
    plt.legend()
    plt.grid(True)
    
    # Guardar el gráfico en la carpeta especificada
    file_path = os.path.join(output_folder, f'{ingredient_name}_forecast.png')
    plt.savefig(file_path)
    plt.close()
    print(f'Gráfico de pronóstico guardado en: {file_path}')

def intercalated_validation(data, model_order=(1,1,1), seasonal_order=(1,1,1,52), test_interval=4):
    """
    Realiza validación intercalada para calcular la precisión del modelo.
    """
    results = {}
    for column in data.columns:
        series = data[column].dropna()
        test_indices = list(range(0, len(series), test_interval))  # Índices para prueba
        predictions = []
        actuals = []

        for i in test_indices:
            # Datos de entrenamiento
            train_data = series.drop(series.index[i:i+1])  # Excluir la semana de prueba
            
            # Ajustar el modelo
            model = SARIMAX(
                train_data, 
                order=model_order, 
                seasonal_order=seasonal_order, 
                enforce_stationarity=False, 
                enforce_invertibility=False
            )
            result = model.fit(disp=False)
            
            # Realizar pronóstico para la semana de prueba
            forecast = result.forecast(steps=1)
            predictions.append(forecast.iloc[0])
            actuals.append(series.iloc[i])
        
        # Cálculo de métricas
        mae = mean_absolute_error(actuals, predictions)
        rmse = np.sqrt(mean_squared_error(actuals, predictions))
        results[column] = {'MAE': mae, 'RMSE': rmse}
        print(f"Resultados para {column}: MAE={mae:.2f}, RMSE={rmse:.2f}")
    
    return results

# Cargar el archivo de datos de ejemplo
filepaths = ['weekly_ingredients.csv']  # Ajusta el nombre del archivo según corresponda

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


# Cargar los datos
filepath = 'weekly_ingredients.csv'
data = load_data(filepath)

# Ejecutar validación intercalada
metrics = intercalated_validation(data)