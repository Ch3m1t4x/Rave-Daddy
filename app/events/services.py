from datetime import date
from .models import Ciudad, Evento,EventoDetalle, Artista, Genero
from events.meteorologia.meteo_api import get_weather_city

# Eventos General
MESES = {
"Ene": 1,
"Feb": 2,
"Mar": 3,
"Abr": 4,
"May": 5,
"Jun": 6,
"Jul": 7,
"Ago": 8,
"Sep": 9,
"Oct": 10,
"Nov": 11,
"Dic": 12,
}
def parsear_fecha(fecha_str):
    dia_str, mes_str = fecha_str.split(" ")

    dia = int(dia_str)
    mes = MESES[mes_str]
    
    hoy = date.today()
    anio = hoy.year
    if mes < hoy.month:
        anio += 1

    return date(anio, mes, dia)

def guardar_eventos_general(ciudad_nombre, fiestas):
    Evento.objects.filter(fecha__lt=date.today()).delete()
    # Verifica si la ciudad ya existe o la crea
    ciudad, _ = Ciudad.objects.get_or_create(nombre=ciudad_nombre)

    for fecha, eventos in fiestas.items():
        fecha_limpia = parsear_fecha(fecha)
        for nombre_fiesta, detalles in eventos.items():
            # Crea el evento
            evento, _ = Evento.objects.get_or_create(
                enlace=detalles["link"],
                defaults={
                    "ciudad":ciudad,
                    "nombre":nombre_fiesta,
                    "club":detalles['club'],
                    "fecha":fecha_limpia,
                    "enlace":detalles['link']
                }
            )
            
def get_events(ciudad):
    ciudad_obj = Ciudad.objects.get(nombre = ciudad.lower())
    eventos = Evento.objects.filter(ciudad=ciudad_obj)
    bot = {}
    for evento in eventos:
        bot[evento.nombre] = {
            "name": evento.nombre,
            "fecha": evento.fecha,
            "Club": evento.club,
        }
    return bot

# Eventos detalle

def guardar_evento_detalles(data, evento_detalle):
    
    evento_detalle.horario = data.get("schedule", "")
    evento_detalle.precio = data.get("price", "")
    evento_detalle.event_info = data.get("event_info", "").strip()
    evento_detalle.club_info = data.get("club_info", "").strip()

    if data.get("djs"):
        artistas_obj = obtener_o_crear_artistas(data.get("djs"), evento_detalle)
        evento_detalle.artistas.set(artistas_obj)
    if data.get("genres"):
        generos_objs = obtener_o_crear_generos(data.get("genres"))
        evento_detalle.generos.set(generos_objs)
    
    evento_detalle.save()
    print(f"{str(evento_detalle.evento)} Hecho")
    
def get_events_details(name):
    e_obj = Evento.objects.get(nombre__icontains = name)
    e_obj_det = EventoDetalle.objects.get(evento = e_obj)
    temp = get_weather_city(e_obj.id)
    
    return str(e_obj_det) + temp
    
# Generos 
def obtener_o_crear_generos(generos):
    genero_objs = []
    for g in generos:
        genero_obj, _ = Genero.objects.get_or_create(nombre=g)
        genero_objs.append(genero_obj)
    return genero_objs

# Artistas
def obtener_o_crear_artistas(artistas, obj_detalle):
    evento = obj_detalle.evento
    artistas_objs = []
    for a in artistas:
        artista_obj, _ = Artista.objects.get_or_create(nombre=a)
        artista_obj.eventos.add(evento)
        artistas_objs.append(artista_obj)
    return artistas_objs

def actualizar_artistas(data, nombre):
    artista, _ = Artista.objects.update_or_create(
        nombre = nombre,
        defaults={
            "info": data.get("info", "")
        }
    )
    if data.get("genres"):
        generos_objs = obtener_o_crear_generos(data.get("genres"))
        artista.generos.set(generos_objs)
        
    print(f"{artista.nombre} Hecho")

def get_artistas(name):
    a_obj = Artista.objects.get(nombre__icontains = name)
    
    