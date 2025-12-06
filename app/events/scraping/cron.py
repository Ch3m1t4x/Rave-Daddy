# python manage.py crontab run fe7d3374024399a685203f6c5e6e168e
def buscar_eventos():
    from .xceed import scraping_xceed_general
    scraping_xceed_general('madrid')
    scraping_xceed_general('barcelona')
    scraping_xceed_general('valencia')
    