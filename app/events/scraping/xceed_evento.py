from playwright.sync_api import sync_playwright

def limpiar_formato(texto, formato):
    fecha = texto.split(formato)
    fecha_limpia = fecha[-1].strip()
    return fecha_limpia

def scraping_xceed_events(link, titulo):
    informacion = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://xceed.me/{link}")

        h1_element = page.locator("h1")
        count = h1_element.count()

        for i in range(count):
            texto = h1_element.nth(i).inner_text().strip()
            if texto == titulo:
                titulo_h1 = h1_element.nth(i)
                print(titulo_h1.inner_text())
                break
        if titulo_h1:
            horario_html = titulo_h1.locator("xpath=following-sibling::p[1]")
            horario = horario_html.inner_text()
            informacion["schedule"] = limpiar_formato(horario,",")
        
        span_precio = page.get_by_test_id("event-tickets-header").get_by_text("€", exact=False)
        precio = span_precio.text_content()
        informacion["price"] = f"Desde {limpiar_formato(precio," ")}"
        browser.close()
    return informacion
"""
    # Dentro de ese ancestro, seleccionar el segundo div hijo (que contiene los enlaces)
    contenedor_enlaces = contenedor_ancestro.locator("div").nth(2)  # nth(1) = segundo div
    enlaces = contenedor_enlaces.locator("a")
    total_enlaces = enlaces.count()

    for i in range(total_enlaces):
        enlace = enlaces.nth(i)
        texto = enlace.inner_text()
        href = enlace.get_attribute("href")
        partes = texto.split("\n")
        print(f"\nFiesta #{i+1}")
        print(f"Fiesta: {partes[0]}")
        print(f"Discoteca: {partes[1]}")
        print(f"Enlace: {href}")

        # Para buscar por clase
        # hijos_clase = enlace.locator(".nombre-de-la-clase")  # Selecciona hijos con esa clase
        # total = hijos_clase.count()
        # for i in range(total):
        #     print(hijos_clase.nth(i).inner_text())


        # hijos = enlace.locator("*")  # Todos los hijos
        # total_hijos = hijos.count()  # Todos los nodos hijos del <a>
        # for i in range(total_hijos):
        #     hijo = hijos.nth(i)
        #     try:
        #         textos[i] = hijo.inner_text()
        #     except Exception as e:    
        #         print(f"Hijo #{i} no es html", e)
    # print(textos)
else:
    print("No se encontró ningún h2 que empiece con 'Hoy'.")
"""