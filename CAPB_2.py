import pandas as pd
import plotly.express as px
import json
import requests

# Leer el archivo Excel asegurando que FIPS sea tratado como texto
try:
    df = pd.read_excel('Book7.xlsx', sheet_name='Sheet1', dtype={"FIPS": str})
    df['FIPS'] = df['FIPS'].str.zfill(5)  # Asegurar que los códigos FIPS tengan 5 caracteres
    print("Archivo Excel leído correctamente.")
    print(df.head())  
except Exception as e:
    print(f"Error al leer el archivo Excel: {e}")
    exit()

# Verificar que las columnas necesarias estén presentes
required_columns = ['County', 'Capacity(MW)', 'FIPS']
if not all(column in df.columns for column in required_columns):
    print(f"El archivo Excel debe contener las columnas: {required_columns}")
    exit()


# Cargar el GeoJSON con los condados de EE.UU.
geojson_url = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
geojson_data = requests.get(geojson_url).json()

# Crear el mapa
try:
    # min_value = df['Capacity(MW)'].min()
    # max_value = df['Capacity(MW)'].max() * 1.2
    fig = px.choropleth(
        df,
        geojson=geojson_data,  # GeoJSON con los condados
        locations='FIPS',  # Usar la columna con los códigos FIPS
        color='Capacity(MW)',  
        scope="usa",
        title='Battery Energy Capacity by County in the United States 2024',
        color_continuous_scale= px.colors.sequential.thermal, #'thermal',#px.colors.sequential.Plasma,
        hover_name='County',
        hover_data=['Capacity(MW)']
    )

 
    # Mostrar el mapa
    fig.show()
    print("Mapa generado correctamente.")
except Exception as e:
    print(f"Error al generar el mapa: {e}")
