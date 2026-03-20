import folium

def generar_mapa_alertas(lista_predicciones):
    """
    Genera un mapa web interactivo que muestra ÚNICAMENTE la predicción de la IA.
    """
    print("🗺️ Generando mapa predictivo...")
    
    mapa_peru = folium.Map(location=[-9.19, -75.01], zoom_start=5, tiles='cartodbpositron')
    
    for alerta in lista_predicciones:
        lat = alerta['lat']
        lon = alerta['lon']
        probabilidad = alerta['probabilidad']
        
        if probabilidad >= 50:
            color_marcador = 'red'
        elif probabilidad >= 20:
            color_marcador = 'orange'
        else:
            color_marcador = 'green'
            
        # Un diseño súper simple y limpio
        texto_popup = f"""
        <div style='width: 180px; text-align: center; font-family: sans-serif;'>
            <h4 style='color:{color_marcador};'><b>Riesgo Sísmico (>5.0)</b></h4>
            <h2 style='margin: 10px 0;'>{probabilidad:.2f}%</h2>
            <small>Próximos 7 días</small>
            
            <hr style='border: 0; border-top: 1px solid #ddd; margin: 10px 0;'>
            <small style='color: #555;'>
                <b>Hora pico histórica:</b><br>
                {alerta['hora_frecuente']} 
            </small>
        </div>
        """
        
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(texto_popup, max_width=200),
            icon=folium.Icon(color=color_marcador, icon='info-sign')
        ).add_to(mapa_peru)
    
    nombre_archivo = "mapa_predicciones_peru.html"
    mapa_peru.save(nombre_archivo)
    print(f"✅ Mapa predictivo generado: {nombre_archivo}")