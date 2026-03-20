import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from datetime import timedelta

def predecir_sismo_semanal(df_zona):
    """Entrena un Random Forest para predecir sismos y devuelve el riesgo y la ventana de tiempo."""
    df_ts = df_zona.set_index('fecha_hora')

    hora_historica = "Sin datos"
    if not df_ts.empty:
        # .hour extrae la hora, .mode() saca la más frecuente
        horas_frecuentes = pd.Series(df_ts.index.hour).mode() 
        if not horas_frecuentes.empty:
            hora_pico = horas_frecuentes[0]
            # Le damos formato bonito, ej: "02:00 hrs"
            hora_historica = f"{hora_pico:02d}:00 hrs"
    
    # 1. Agrupar por semanas ('W')
    features = df_ts.resample('W').agg({'magnitud': ['count', 'max'], 'energia_joules': 'sum'})
    features.columns = ['num_sismos_sem', 'mag_max_sem', 'energia_total_sem']
    features = features.fillna(0)
    
    # 2. Ventanas de tiempo (últimas 4 semanas)
    features['sismos_ultimas_4sem'] = features['num_sismos_sem'].rolling(window=4).sum()
    features['energia_acum_4sem'] = features['energia_total_sem'].rolling(window=4).sum()
    dataset_ia = features.dropna().copy()
    
    # 3. Preparar variables para la IA
    dataset_ia['target_proxima_sem'] = (dataset_ia['mag_max_sem'].shift(-1) >= 5.0).astype(int)
    
    datos_historicos = dataset_ia.dropna()
    datos_hoy = dataset_ia.tail(1).drop(columns=['target_proxima_sem'])
    
    if datos_hoy.empty:
        return 0.00, "Sin datos históricos en esta zona", "N/A"
    
    # --- CALCULAMOS LA VENTANA DE TIEMPO (LA PRÓXIMA SEMANA) ---
    fecha_base = datos_hoy.index[0] # Esta es la fecha del último bloque de datos
    fecha_inicio_alerta = fecha_base
    fecha_fin_alerta = fecha_base + timedelta(days=7)
    
    texto_ventana = f"Del {fecha_inicio_alerta.strftime('%d/%m/%Y')} al {fecha_fin_alerta.strftime('%d/%m/%Y')}"
    
    
    X = datos_historicos[['num_sismos_sem', 'energia_total_sem', 'sismos_ultimas_4sem', 'energia_acum_4sem']]
    y = datos_historicos['target_proxima_sem']
    
    if len(X) == 0:
        return 0.0, texto_ventana, hora_historica # Devolvemos riesgo cero y la fecha
    
    # 4. Entrenar y predecir
    modelo_rf = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo_rf.fit(X, y)
    
    variables_hoy = datos_hoy[['num_sismos_sem', 'energia_total_sem', 'sismos_ultimas_4sem', 'energia_acum_4sem']]
    probabilidades = modelo_rf.predict_proba(variables_hoy)[0]
    
    if 1 in modelo_rf.classes_:
        indice_clase_1 = list(modelo_rf.classes_).index(1)
        riesgo = probabilidades[indice_clase_1] * 100
    else:
        riesgo = 0.0 
        
    return riesgo, texto_ventana, hora_historica # Ahora la función devuelve DOS cosas

    