import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def cargar_y_limpiar_datos(ruta_archivo):
    """Carga el Excel del IGP, limpia fechas y calcula energía."""
    print("🧹 Limpiando base de datos...")
    df = pd.read_excel(ruta_archivo)
    df.columns = ['fecha', 'hora', 'latitud', 'longitud', 'profundidad', 'magnitud']
    
    tiempo_texto = df['fecha'].astype(str) + ' ' + df['hora'].astype(str)
    df['fecha_hora'] = pd.to_datetime(tiempo_texto, format='mixed')
    
    # Nos quedamos con lo importante y calculamos Joules
    df = df.dropna(subset=['magnitud', 'latitud', 'longitud']).copy()
    df['energia_joules'] = 10 ** (4.8 + 1.5 * df['magnitud'])
    
    columnas = ['fecha_hora', 'latitud', 'longitud', 'profundidad', 'magnitud', 'energia_joules']
    return df[columnas]