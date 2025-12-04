from models import Artista, Ciudad, Evento, EventoDetalle, Genero

# Crear una ciudad, género, artista, etc.
ciudad = Ciudad.objects.create(nombre="Barcelona")
genero = Genero.objects.create(nombre="Techno")
artista = Artista.objects.create(nombre="DJ Example", enlace="https://example.com")
evento = Evento.objects.create(nombre="Fiesta en Barcelona", ciudad=ciudad, fecha="2025-12-12", enlace="https://evento.com")
evento_detalle = EventoDetalle.objects.create(evento=evento, horario="00:00", precio="10€", event_info="Información del evento", club_info="Club XYZ")
evento_detalle.artistas.add(artista)
evento_detalle.generos.add(genero)