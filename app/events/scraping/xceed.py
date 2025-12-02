from playwright.sync_api import sync_playwright

textos = {}
dias = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://xceed.me/es/madrid/events")  # Cambia por tu URL

    # Localizar todos los h2 y filtrar el que comienza con "Hoy"


    h2_elements = page.locator("h2")
    count = h2_elements.count()

    fecha_h2 = None
    for i in range(count):
        texto = h2_elements.nth(i).inner_text().strip()
        if texto.endswith("Dic"):
            dias.append(h2_elements.nth(i))
            print(h2_elements.nth(i).inner_text())
            # Mirar para guardar el texto por un lado y el pointer en otro
            
    for dia in dias:
        print(dia.inner_text())
        contenedor_ancestro = dia.locator("xpath=ancestor::div[3]")
        
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

    browser.close()
