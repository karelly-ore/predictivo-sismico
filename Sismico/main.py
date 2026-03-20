from limpieza_datos import cargar_y_limpiar_datos
from analisis_espacial import encontrar_zonas_riesgo
from modelo_ia import predecir_sismo_semanal
from mapa_interactivo import generar_mapa_alertas

print("="*50)
print("🚀 INICIANDO SISTEMA DE PREDICCIÓN SÍSMICA")
print("="*50)

df_nacional = cargar_y_limpiar_datos("catalogo_sismico.xlsx")
zonas_criticas = encontrar_zonas_riesgo(df_nacional, top_n=10)

print("\n🤖 CALCULANDO PREDICCIONES PARA LA PRÓXIMA SEMANA...")
print("-" * 50)

resultados_para_el_mapa = []

for id_celda, datos_celda in zonas_criticas.iterrows():
    lat = datos_celda['lat_celda']
    lon = datos_celda['lon_celda']
    
    df_esta_zona = df_nacional[
        (df_nacional['latitud'].round(1) == lat) & 
        (df_nacional['longitud'].round(1) == lon)
    ]
    
    # 💥 Aquí ocurre la magia: La IA calcula el porcentaje
    probabilidad_riesgo, ventana_fechas, hora_promedio = predecir_sismo_semanal(df_esta_zona)
    
    # Solo guardamos lo básico: dónde y cuál es el riesgo
    resultados_para_el_mapa.append({
        'lat': lat,
        'lon': lon,
        'probabilidad': probabilidad_riesgo,
        'fechas': ventana_fechas,
        'hora_frecuente':hora_promedio
    })
    
    print(f"Zona [Lat: {lat}, Lon: {lon}] -> Riesgo: {probabilidad_riesgo:.2f}% ({ventana_fechas})")

print("-" * 50)
generar_mapa_alertas(resultados_para_el_mapa)
print("✅ ANÁLISIS FINALIZADO")