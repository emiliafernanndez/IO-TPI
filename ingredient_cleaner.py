import pandas as pd
import os

def clean_ingredient_data(input_file, output_file='cleaned_ingredient_data.csv'):
    """
    Limpia los datos de ingredientes cargados desde un archivo CSV y guarda el resultado en otro archivo.

    Parámetros:
    input_file (str): Ruta al archivo CSV de ingredientes a limpiar.
    output_file (str): Ruta del archivo CSV de salida con los datos limpios.
    """

    # Cargar el archivo
    data = pd.read_csv(input_file, encoding='ISO-8859-1')

    # Eliminar las columnas vacías
    data.dropna(axis=1, how='all', inplace=True)

    # Lista de nuevos nombres para las columnas
    nuevos_nombres = [
        "TRADITIONAL BAGUETTE", "FORMULE SANDWICH", "CROISSANT", "PAIN AU CHOCOLAT", "BANETTE",
        "BAGUETTE", "SANDWICH COMPLET", "SPECIAL BREAD TRAITEUR", "GRAND FAR BRETON", "TARTELETTE",
        "CEREAL BAGUETTE", "VIK BREAD", "BRIOCHE", "GD KOUIGN AMANN", "CAMPAGNE", "BOULE 400G",
        "ECLAIR", "MOISSON", "SAND JB EMMENTAL", "COMPLET", "KOUIGN AMANN", "PAIN BANETTE",
        "DIVERS VIENNOISERIE", "FINANCIER X5"
    ]

    # Renombrar las columnas (omitiendo la primera columna)
    data.columns = [data.columns[0]] + nuevos_nombres

    # Establecer la primera columna como índice antes de transponer
    data.set_index(data.columns[0], inplace=True)

    # Transponer el DataFrame
    data = data.T

    # Rellenar los valores nulos con 0
    for column in data.columns:
        data[column] = data[column].fillna(0)

    # Verificar si el archivo de salida existe, si no, crear el directorio
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Guardar el DataFrame limpio
    data.to_csv(output_file)

    print(f'Datos limpiados guardados en {output_file}')
