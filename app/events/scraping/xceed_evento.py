from playwright.sync_api import sync_playwright
from events.models import Evento, EventoDetalle
from events.services import guardar_evento_detalles

def limpiar_formato(texto, formato):
    separado = texto.split(formato)
    texto_limpio = separado[-1].strip()
    return texto_limpio
    
def scraping_xceed_events(enlace):
    evento = Evento.objects.get(enlace = enlace)
    evento_detalle, buscar = EventoDetalle.objects.get_or_create(evento = evento)
    if buscar:
        informacion = {}
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(enlace)

            # Busca la informacion sobre el horario de la fiesta
            horario = page.locator("header").locator("p").inner_text()
            informacion["schedule"] = limpiar_formato(horario,",")

            try:
                span_precio = page.get_by_test_id("event-tickets-header").get_by_text("€", exact=False)
                precio = span_precio.text_content()
                informacion["price"] = f"Desde {limpiar_formato(precio," ")}"
            except:
                informacion['price'] = "Apuntate por listas"
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
                informacion['genres'] = [g.strip() for g in generos_raw[0].split("\n") if g.strip()]

            # Busca informacion si hay sobre los artistas
            informacion['djs'] = []
            lineup_div = page.locator("//*[@data-section='lineup']/div").first
            artistas_textos = lineup_div.locator("a")
            if artistas_textos.count():
                artistas_textos = artistas_textos.all_inner_texts()
                informacion['djs'] = [ nombre.split("\n")[0] for nombre in artistas_textos ]
            browser.close()
        guardar_evento_detalles(informacion, evento_detalle)
    else:
        print(f"{evento.nombre} Ya estaba")