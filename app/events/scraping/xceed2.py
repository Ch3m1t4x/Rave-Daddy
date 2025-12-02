from playwright.sync_api import sync_playwright

textos = {}

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
        if texto.startswith("Hoy"):
            fecha_h2 = h2_elements.nth(i)
            print(fecha_h2.inner_text())
            break

    if fecha_h2:
        # Subir dos niveles de div desde el h2
        contenedor_ancestro = fecha_h2.locator("xpath=ancestor::div[3]")
        
        # Dentro de ese ancestro, seleccionar el segundo div hijo (que contiene los enlaces)
        contenedor_enlaces = contenedor_ancestro.locator("div").nth(2)  # nth(1) = segundo div
        enlaces = contenedor_enlaces.locator("a")
        total_enlaces = enlaces.count()

        for i in range(total_enlaces):
            enlace = enlaces.nth(i)
            texto = enlace.inner_text()
            href = enlace.get_attribute("href")
            partes = texto.split("\n")
            print(f"\nFiesta #{i}")
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

    browser.close()
