import requests
from events.models import Evento, EventoDetalle
from datetime import timedelta, datetime


def get_weather_city(id_e):
    evento = Evento.objects.get(id = id_e)
    ciudad = evento.ciudad.nombre
    fecha = evento.fecha.isoformat()
    ini_str , fin_str = EventoDetalle.objects.get(evento = evento).horario.split(" - ")
    h_ini = datetime.strptime(ini_str, "%I:%M%p").time().hour
    h_fin = datetime.strptime(fin_str, "%I:%M%p").time().hour
    h_ini = int(h_ini)-1
    h_fin = int(h_fin)+1
    
    # Primero: Convertimos ciudad a lat/lon
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": ciudad, "count": 1, "language": "es"}
    ).json()

    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]
    timezone = geo["results"][0]["timezone"]

    # Primero cogemos la temperatura del dia de la fiesta
    t_dia = requests.get(
    "https://api.open-meteo.com/v1/forecast",
    params={
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m",
        "timezone": timezone,
        "start_date": fecha,
        "end_date": fecha
    }
    ).json()
    
    t_dia_horas = t_dia["hourly"]["temperature_2m"][h_ini:]
    
    fecha = evento.fecha + timedelta(days=1)
    fecha = fecha.isoformat()

    # Buscamos las temperaturas de la noche del dia siguiente
    t_noche = requests.get(
    "https://api.open-meteo.com/v1/forecast",
    params={
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m",
        "timezone": timezone,
        "start_date": fecha,
        "end_date": fecha
    }
    ).json()
        
    t_noche_horas = t_noche["hourly"]["temperature_2m"][:h_fin]
    
    horas_dia = [h_ini + i for i in range(len(t_dia_horas))]

    horas_noche = [i for i in range(len(t_noche_horas))]
    
    horas_totales = [(h % 24) for h in (horas_dia + horas_noche)]
    temps_totales = t_dia_horas + t_noche_horas

    temp_formateadas = []

    # Inicializamos con None para que la primera siempre se guarde
    temp_anterior = None

    for h, t in zip(horas_totales, temps_totales):
        t_decena = int(t)
        if t_decena != temp_anterior:
            temp_formateadas.append(f"{h}h: {t}ºC")
            temp_anterior = t_decena
    salida = ", ".join(temp_formateadas)
    return "\nTemperaturas:\n" + salida