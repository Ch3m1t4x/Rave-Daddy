from playwright.sync_api import sync_playwright
from events.services import actualizar_artistas
    
# def nombre_url(name):
#     name = name.replace(".", " ")
#     name = name.replace(" ","-")
#     name = name.lower()
#     return name

def scraping_xceed_artist(name, enlace):
    artista = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://xceed.me/{enlace}")
        
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
    actualizar_artistas(artista,name)
    return artista