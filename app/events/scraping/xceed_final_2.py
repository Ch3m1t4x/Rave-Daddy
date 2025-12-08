from playwright.sync_api import sync_playwright

def limpiar_fecha(texto):
    fecha = texto.split(",")
    fecha_limpia = fecha[-1].strip()
    return fecha_limpia

def scraping_xceed_general(ciudad):
    fiestas = {}
    dias = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://xceed.me/es/{ciudad.lower()}/events")

        # Localizar todos los h2 y filtrar el que comienza con "Hoy"


        h2_elements = page.locator("h2")
        count = h2_elements.count()

        fecha_h2 = None
        for i in range(count):
            texto = h2_elements.nth(i).inner_text().strip()
            if texto.endswith("Dic"):
                fecha = limpiar_fecha(texto)
                dias.append(h2_elements.nth(i))
                fiestas[fecha]={}
                # Mirar para guardar el texto por un lado y el pointer en otro
        for dia in dias:
            dia_fecha = limpiar_fecha(dia.inner_text())
            
            contenedor_ancestro = dia.locator("xpath=ancestor::div[3]")
            
            contenedor_enlaces = contenedor_ancestro.locator("div").nth(2)  # nth(1) = segundo div
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
                    "discoteca": discoteca,
                    "enlace": href
                }

        browser.close()
        if fiestas == {}:
            fiestas = f"No hay fiestas en {ciudad}"
    return fiestas

print(scraping_xceed_general("murcia"))