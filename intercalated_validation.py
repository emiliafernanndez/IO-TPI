import os
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings
from utils import crear_carpeta

warnings.filterwarnings("ignore")

def load_data(filepath):
    """Carga los datos desde un archivo CSV."""
    data = pd.read_csv(filepath, index_col=0, parse_dates=True, encoding='utf-8-sig')
    return data

def format_week_interval(weeks):
    """Formatea un conjunto de semanas en un intervalo [inicio, fin]."""
    return f"[{weeks[0].strftime('%Y-%m-%d')}, {weeks[-1].strftime('%Y-%m-%d')}]"

def intercalated_validation(data, model_order=(1, 1, 1), seasonal_order=(1, 1, 1, 52), 
                            train_weeks=4, test_weeks=2, output_folder='error_prediction'):
    """Realiza validación intercalada con ventanas consecutivas de entrenamiento y prueba."""
    
    # Crear carpeta de salida si no existe
    crear_carpeta(output_folder)
    
    for column in data.columns:
        series = data[column].dropna()
        results = []
        start_idx = 0
        
        while start_idx + train_weeks + test_weeks <= len(series):
            # Definir semanas de entrenamiento y prueba consecutivas
            train_data = series.iloc[start_idx:start_idx + train_weeks]
            test_data = series.iloc[start_idx + train_weeks:start_idx + train_weeks + test_weeks]
            
            # Registrar el intervalo de semanas
            train_interval = format_week_interval(train_data.index)
            test_interval = format_week_interval(test_data.index)
            
            # Ajustar el modelo y realizar predicciones
            model = SARIMAX(
                train_data, 
                order=model_order, 
                seasonal_order=seasonal_order, 
                enforce_stationarity=False, 
                enforce_invertibility=False
            )
            result = model.fit(disp=False)
            forecast = result.forecast(steps=test_weeks)
            
            # Calcular RMSE (Root Mean Squared Error)
            squared_errors = (test_data - forecast) ** 2
            rmse = np.sqrt(np.mean(squared_errors))
            
            # Guardar resultados
            results.append({
                'Train Weeks': train_interval,
                'Test Weeks': test_interval,
                'Avg Actual Value': test_data.mean(),
                'Avg Predicted Value': forecast.mean(),
                'Error (RMSE)': rmse
            })
            
            # Desplazar la ventana completamente (entrenamiento + prueba)
            start_idx += train_weeks + test_weeks
        
        # Guardar resultados en un archivo CSV
        results_df = pd.DataFrame(results)
        output_path = os.path.join(output_folder, f'{column}_error_prediction.csv')
        results_df.to_csv(output_path, index=False)
        print(f"Archivo generado para {column}: {output_path}")

# Cargar los datos
filepath = 'weekly_ingredients.csv'  # Cambia el nombre del archivo según corresponda
data = load_data(filepath)

# Ejecutar validación intercalada con ventanas de 4 semanas de entrenamiento y 2 de prueba
intercalated_validation(data, train_weeks=4, test_weeks=2, output_folder='error_prediction')
