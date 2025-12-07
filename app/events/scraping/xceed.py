from datetime import date
from events.models import Ciudad, Evento

MESES = {
    "Ene": 1,
    "Feb": 2,
    "Mar": 3,
    "Abr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Ago": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dic": 12,
}

def parsear_fecha(fecha_str):
    dia_str, mes_str = fecha_str.split(" ")

    dia = int(dia_str)
    mes = MESES[mes_str]
    
    hoy = date.today()
    anio = hoy.year
    if mes < hoy.month:
        anio += 1

    return date(anio, mes, dia)

def limpiar_formato(texto):
    fecha = texto.split(",")
    fecha_limpia = fecha[-1].strip()
    return fecha_limpia

def get_events(ciudad):
    ciudad_obj = Ciudad.objects.get(nombre = ciudad.lower())
    eventos = Evento.objects.filter(ciudad=ciudad_obj)
    bot = {}
    for evento in eventos:
        fecha_str = evento.fecha.strftime("%Y-%m-%d")
        partes = evento.enlace.split("/")
        url_sin_ultimo = partes[-2]
        if fecha_str not in bot:
            bot[fecha_str] = {}
        bot[fecha_str][evento.nombre] = {
            "name": evento.nombre,
            "dame_detalles_input": f"/{url_sin_ultimo}/",
            "More": f"Club : {evento.club}"
        }

    return bot

def guardar_eventos_general(ciudad_nombre, fiestas):
    Evento.objects.filter(fecha__lt=date.today()).delete()
    # Verifica si la ciudad ya existe o la crea
    ciudad, _ = Ciudad.objects.get_or_create(nombre=ciudad_nombre)

    for fecha, eventos in fiestas.items():
        fecha_limpia = parsear_fecha(fecha)
        for nombre_fiesta, detalles in eventos.items():
            # Crea el evento
            evento, _ = Evento.objects.get_or_create(
                enlace=detalles["link"],
                defaults={
                    "ciudad":ciudad,
                    "nombre":nombre_fiesta,
                    "club":detalles['club'],
                    "fecha":fecha_limpia,
                    "enlace":detalles['link']
                }
            )

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