from playwright.sync_api import sync_playwright
# from events.models import Evento, EventoDetalle, Artista, Genero

def obtener_o_crear_generos(generos):
    genero_objs = []
    for g in generos:
        genero_obj, _ = Genero.objects.get_or_create(nombre=g)
        genero_objs.append(genero_obj)
    return genero_objs

def obtener_o_crear_generos(artistas, link):
    evento = Evento.objects.get(enlace=link)
    artistas_objs = []
    for a in artistas:
        artista_obj, _ = Artista.objects.get_or_create(nombre=a.get("artist_name"), enlace=a.get("artist_link"))
        artistas_objs.append(artista_obj)
    return artistas_objs
    
def guardar_evento_detalles(link, data):

    evento = Evento.objects.get(enlace=link)

    detalle, _ = EventoDetalle.objects.get_or_create(
        evento = evento,
        defaults={
            "horario": data.get("schedule", ""),
            "precio": data.get("price", ""),
            "event_info": data.get("event_info", ""),
            "club_info": data.get("club_info", "")
        }
    )
    if data.get("djs"):
        artistas_obj = obtener_o_crear_generos(data.get("djs"))
        detalle.artistas.set(artistas_obj)
    if data.get("genres"):
        generos_objs = obtener_o_crear_generos(data.get("genres"))
        detalle.generos.set(generos_objs)

def limpiar_formato(texto, formato):
    separado = texto.split(formato)
    texto_limpio = separado[-1].strip()
    return texto_limpio

def tratar_info(info):
    partes = [
        f"Schedule: {info.get('schedule')}",
        f"Price: {info.get('price')}"
    ]
    if info.get("club_info") != "No hay información del club":
        partes.append(f"Information about the club: {info.get('club_info')}")
    
    if info.get("event_info") != "No hay información de la fiesta":
        partes.append(f"Information about the event: {info.get('event_info')}")
    
    if info.get("genres"):
        generos = "Genres of the event: " + ", ".join(info.get("genres"))
        partes.append(generos)

    if info.get("djs"):
        artistas = "DJs of the event: " + ", ".join(info.get("djs"))
        partes.append(artistas)

    return "\n".join(partes)

def scraping_xceed_events(link):
    informacion = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(link)
                                        # mirar si sacar los precios de todas las entradas
                                        
        # Busca la informacion sobre el horario de la fiesta
        horario = page.locator("header").locator("p").inner_text()
        informacion["schedule"] = limpiar_formato(horario,",")
        
        span_precio = page.get_by_test_id("event-tickets-header").get_by_text("€", exact=False)
        precio = span_precio.text_content()
        informacion["price"] = f"Desde {limpiar_formato(precio," ")}"
        
        # Busca informacion si hay sobre el club  
        club_html = page.locator("//*[@id='venue']").get_by_test_id("expandable-text-content")
        informacion['club_info'] = club_html.inner_text() if club_html.count() else "No hay información del club"
        
        # Busca la informacion si hay sobre el evento
        info_html = page.locator("//*[@id='about']").get_by_test_id("expandable-text-content")
        informacion["event_info"] = info_html.inner_text() if info_html.count() else "No hay información de la fiesta"
        
        # Busca la informacion de los generos si la hay
        informacion['genres'] = []
        info_html = page.locator("[data-testid='event-tickets-button'] > div").first
        if info_html.count():
            genero_html = info_html.locator("div > div").first
            generos_raw = genero_html.all_inner_texts()
            generos = [g.strip() for g in generos_raw[0].split("\n") if g.strip()]
        informacion['genres'] = generos
        
        # Busca informacion si hay sobre los artistas
        informacion['djs'] = []
        lineup_div = page.locator("//*[@data-section='lineup']/div").first
        artistas_textos = lineup_div.locator("a")
        if artistas_textos.count():
            artistas_textos = artistas_textos.all_inner_texts()
            informacion['djs'] = [ nombre.split("\n")[0] for nombre in artistas_textos ]
        browser.close()
    # guardar_evento_detalles(link, informacion)
    # return tratar_info(informacion)
    return informacion
