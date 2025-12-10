from playwright.sync_api import sync_playwright
from events.models import Artista, Genero

def obtener_o_crear_generos(generos):
    genero_objs = []
    for g in generos:
        genero_obj, _ = Genero.objects.get_or_create(nombre=g)
        genero_objs.append(genero_obj)
    return genero_objs


def guardar_artista(data, generos):
    artista, _ = Artista.objects.update_or_create(
        defaults={
            "info": data.get("info", "")
        }
    )
    if generos:
        generos_objs = obtener_o_crear_generos(generos)
        artista.generos.set(generos_objs)
    
def nombre_url(name):
    name = name.replace(".", " ")
    name = name.replace(" ","-")
    name = name.lower()
    return name
    #Mirar para hacer un modelo genero que este conectado con fiestas

def scraping_xceed_artist(name):
    name = nombre_url(name)
    artista = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://xceed.me/es/artist/{name}")
        
        # Busca los géneros que tiene el artista si los hay
        generos = []
        generos_html = page.get_by_test_id("artist-entity").locator("div").first
        if generos_html.count():
            generos = [g.strip() for g in generos_html.inner_text().split("\n") if g.strip()]
        artista['genres'] = generos
        
        # Busca información del artista si hay
        info_html = page.locator("//*[@id='about']").get_by_test_id("expandable-text-content")
        if info_html.count():
            artista['info'] = info_html.inner_text().strip()
        else:
            artista['info'] = "No hay información del artista"
        
            
            
        browser.close()
        # guardar_artista(artista,generos)
    return artista