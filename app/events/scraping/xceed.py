from datetime import date
from events.services import guardar_eventos_general, MESES

def limpiar_formato(texto):
    fecha = texto.split(",")
    fecha_limpia = fecha[-1].strip()
    return fecha_limpia


def scraping_xceed_general(ciudad):
    from playwright.sync_api import sync_playwright    
    fiestas = {}
    dias = []
    mes = date.today().month
    mes_busqueda = list(MESES.keys())[mes-1]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://xceed.me/es/{ciudad.lower()}/events")

        h2_elements = page.locator("h2")
        count = h2_elements.count()

        for i in range(count):
            texto = h2_elements.nth(i).inner_text().strip()
            if texto.endswith(mes_busqueda):
                fecha = limpiar_formato(texto)
                dias.append(h2_elements.nth(i))
                fiestas[fecha]={}
        for dia in dias:
            dia_fecha = limpiar_formato(dia.inner_text())
            
            contenedor_ancestro = dia.locator("xpath=ancestor::div[3]")
            
            contenedor_enlaces = contenedor_ancestro.locator("div").nth(2)
            enlaces = contenedor_enlaces.locator("a")
            total_enlaces = enlaces.count()
            for i in range(total_enlaces):
                enlace = enlaces.nth(i)
                texto = enlace.inner_text()
                href = enlace.get_attribute("href")
                partes = texto.split("\n")
                nombre_fiesta = partes[0]
                discoteca = partes[1]
                fiestas[dia_fecha][nombre_fiesta] = {
                    "club": discoteca,
                    "link": f"https://xceed.me{href}"
                }

        browser.close()
    guardar_eventos_general(ciudad, fiestas)
    return fiestas