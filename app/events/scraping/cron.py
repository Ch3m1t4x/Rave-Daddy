# python manage.py crontab run fe7d3374024399a685203f6c5e6e168e
def buscar_detalles(fiestas):
    from .xceed_evento import scraping_xceed_events
    for eventos in fiestas.values():
        for detalles in eventos.values():
            scraping_xceed_events(detalles["link"])


def buscar_eventos():
    from .xceed import scraping_xceed_general
    fiestas_madrid = scraping_xceed_general('madrid')
    buscar_detalles(fiestas_madrid)
    fiestas_barcelona = scraping_xceed_general('barcelona')
    buscar_detalles(fiestas_barcelona)
    fiestas_valencia = scraping_xceed_general('valencia')
    buscar_detalles(fiestas_valencia)
    