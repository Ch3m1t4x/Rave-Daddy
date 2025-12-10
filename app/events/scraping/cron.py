# python manage.py crontab run c14792ed7ff856fc46d7849fd03a9606
def buscar_detalles(fiestas):
    from .xceed_evento import scraping_xceed_events
    for eventos in fiestas.values():
        for detalles in eventos.values():
            enlaces_artistas = scraping_xceed_events(detalles["link"])
            if enlaces_artistas:
                buscar_artistas(enlaces_artistas)

def buscar_artistas(artistas):
    from .xceed_artista import scraping_xceed_artist
    for artista in artistas:
        scraping_xceed_artist(artista['nombre'],artista['enlace'])

def buscar_eventos():
    from .xceed import scraping_xceed_general
    fiestas_madrid = scraping_xceed_general('madrid')
    buscar_detalles(fiestas_madrid) 
    fiestas_barcelona = scraping_xceed_general('barcelona')
    buscar_detalles(fiestas_barcelona)
    fiestas_valencia = scraping_xceed_general('valencia')
    buscar_detalles(fiestas_valencia)
    