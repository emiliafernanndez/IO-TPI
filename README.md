# Trabajo Práctico Integrador - Investigación Operativa (2024)
## Optimización de la Gestión de Inventarios en una Panadería Francesa

Este repositorio contiene el desarrollo del **TPI de la cátedra de Investigación Operativa (UTN FRCU, 2024)**. El proyecto se centra en la aplicación de modelos matemáticos y estadísticos para resolver un problema real de gestión de stocks, buscando el equilibrio óptimo entre niveles de servicio y costos operativos.

## Contexto del Proyecto
El objetivo principal consistió en diseñar una política de reabastecimiento óptima para una panadería, basada en datos históricos de ventas. Se abordó el problema desde una perspectiva integral, cubriendo desde el tratamiento de datos crudos hasta la validación de modelos de optimización bajo restricciones físicas y financieras.

## Etapas del Desarrollo

### 1. Análisis Exploratorio y Clasificación ABC
*   **ETL:** Limpieza, normalización y transformación de un dataset histórico (Kaggle).
*   **Segmentación de Insumos:** Aplicación de la técnica **ABC (Ley de Pareto)** para identificar los insumos críticos (Harina de Trigo, Manteca, Sal y Azúcar) que representan el mayor impacto en el costo y la operación.

### 2. Modelado Predictivo (Time Series)
*   **Análisis de Estacionalidad:** Identificación de 4 temporadas críticas en el año.
*   **Pronósticos SARIMA:** Implementación en Python de modelos de series temporales estacionales para predecir la demanda semanal de insumos.
*   **Validación:** Evaluación de precisión mediante métricas de error **RMSE**.

### 3. Optimización de Inventarios
*   **Modelo Determinístico con Stock de Protección:** Desarrollo de un modelo para minimizar el Costo Total Esperado (CTE) en cada temporada.
*   **Cálculo de Parámetros:** Determinación de lotes óptimos de compra ($q$), puntos de reorden y stocks de seguridad para mitigar la aleatoriedad.
*   **Resolución con LINGO:** Implementación del modelo matemático aplicando condiciones de **Karush-Kuhn-Tucker (KKT)** para el manejo de restricciones de volumen de depósito y capital inmovilizado.

### 4. Análisis de Sensibilidad y Simulación
*   **Simulación de Monte Carlo:** Evaluación de la robustez del modelo ante variaciones estocásticas en la demanda y cambios en el tamaño de los lotes, asegurando la viabilidad del plan de inventario propuesto.

## Stack Tecnológico
*   **Modelado Estadístico:** Python (Pandas, Statsmodels, Matplotlib, Seaborn).
*   **Optimización Matemática:** LINGO (Modelado de programación no lineal).
*   **Simulación:** Python (Numpy para simulaciones de Monte Carlo).
