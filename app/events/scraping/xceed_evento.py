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
        if "https://xceed.me/" in link:
            page.goto(link)
        else:    
            page.goto(f"https://xceed.me/{link}")

        h1_element = page.locator("h1")
        count = h1_element.count()

        for i in range(count):
            texto = h1_element.nth(i).inner_text().strip()
            if titulo.split(" ")[0] in texto :
                titulo_h1 = h1_element.nth(i)
                break
        if titulo_h1:
            horario_html = titulo_h1.locator("xpath=following-sibling::p[1]")
            horario = horario_html.inner_text()
            informacion["schedule"] = limpiar_formato(horario,",")
        
        span_precio = page.get_by_test_id("event-tickets-header").get_by_text("€", exact=False)
        precio = span_precio.text_content()
        informacion["price"] = f"Desde {limpiar_formato(precio," ")}"
        
        try:
            h2_element = page.locator("h2")
            count = h2_element.count()
            for i in range(count):
                texto = h2_element.nth(i).inner_text().strip()
                if texto.lower() == "info":
                    h2_titulo = h2_element.nth(i)
            if h2_titulo:
                info_html = h2_titulo.locator("xpath=following-sibling::div[1]")
                info = info_html.inner_text()
                informacion["info"] = info
        except Exception as e: 
            print("No hay info: ",e)     
            
        try:
            h2_titulo2 = h2_element.nth(-1)
            if h2_titulo2:
                club_html = h2_titulo2.locator("xpath=following-sibling::div[1]")
                club = club_html.inner_text()
                informacion["info_club"] = club
        except Exception as e: 
            print("No hay info del club: ",e)   
                
        browser.close()
    return informacion