import pandas as pd

def encontrar_zonas_riesgo(df, top_n=10):
    """Divide el mapa en cuadrículas de 11x11km y encuentra las más peligrosas."""
    print(f"🗺️ Cuadriculando el mapa de Perú...")
    df_mapa = df.copy()
    
    df_mapa['lat_celda'] = df_mapa['latitud'].round(1)
    df_mapa['lon_celda'] = df_mapa['longitud'].round(1)
    df_mapa['id_celda'] = df_mapa['lat_celda'].astype(str) + "_" + df_mapa['lon_celda'].astype(str)
    
    riesgo = df_mapa.groupby('id_celda').agg({
        'magnitud': 'count',
        'energia_joules': 'sum',
        'lat_celda': 'first',
        'lon_celda': 'first'
    }).rename(columns={'magnitud': 'total_sismos'})
    
    top_celdas = riesgo.sort_values(by='energia_joules', ascending=False).head(top_n)
    return top_celdas