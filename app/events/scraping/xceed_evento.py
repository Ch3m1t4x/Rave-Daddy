from playwright.sync_api import sync_playwright
from events.models import Evento, EventoDetalle, Artista, Genero

def obtener_o_crear_generos(generos):
    genero_objs = []
    for g in generos:
        genero_obj, _ = Genero.objects.get_or_create(nombre=g)
        genero_objs.append(genero_obj)
    return genero_objs
    
def guardar_evento_detalles(link, data, artistas, generos):

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
    if artistas:
        detalle.artistas.set(artistas)
    if generos:
        generos_objs = obtener_o_crear_generos(generos)
        detalle.generos.set(generos_objs)

def limpiar_formato(texto, formato):
    separado = texto.split(formato)
    texto_limpio = separado[-1].strip()
    return texto_limpio

def scraping_xceed_events(link):
    informacion = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(link)
                                        # mirar si sacar los precios de todas las entradas
        # Busca la informacion de los generos si la hay
        info_html = page.locator("[data-testid='event-tickets-button'] > div").first
        if info_html.count():
            genero_html = info_html.locator("div > div").first
            generos_raw = genero_html.all_inner_texts()
            generos = [g.strip() for g in generos_raw[0].split("\n") if g.strip()]
            

                                        
        # Busca la informacion sobre el horario de la fiesta
        horario = page.locator("//*[@data-sentry-component='EventHeaderSection']").locator("p").inner_text()
        informacion["schedule"] = limpiar_formato(horario,",")
        
        span_precio = page.get_by_test_id("event-tickets-header").get_by_text("€", exact=False)
        precio = span_precio.text_content()
        informacion["price"] = f"Desde {limpiar_formato(precio," ")}"
        
        # Busca la informacion si hay sobre el evento
        info_html = page.locator("//*[@id='about']").get_by_test_id("expandable-text-content")
        informacion["event_info"] = info_html.inner_text() if info_html.count() else "No hay información de la fiesta"
        
        # Busca informacion si hay sobre el club  
        club_html = page.locator("//*[@id='venue']").get_by_test_id("expandable-text-content")
        informacion['club_info'] = club_html.inner_text() if club_html.count() else "No hay información del club"
        
        # Busca informacion si hay sobre los artistas    
        artistas_evento = []
        lineup_div = page.locator("//*[@data-sentry-component='LineupSection']/div").first
        artistas_html = lineup_div.locator("a")
        for artista_elem in artistas_html.all():
            nombre = artista_elem.inner_text().split("\n")[0]
            enlace = f"https://xceed.me{artista_elem.get_attribute('href')}"
            
            artista_obj, _ = Artista.objects.get_or_create(nombre=nombre, enlace=enlace)
            artistas_evento.append(artista_obj)

                
        browser.close()
    guardar_evento_detalles(link, informacion, artistas_evento, generos)    
    return informacion