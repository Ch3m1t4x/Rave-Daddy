from django.db import models

# Para las ciudades donde se organizan los eventos
class Ciudad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre

# Modelo para almacenar los eventos generales
class Evento(models.Model):
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    club = models.CharField(max_length=200)
    fecha = models.DateField()
    enlace = models.URLField(unique=True)

    def __str__(self):
        return f"Name: {self.nombre}, Date: {self.fecha}, Club: {self.club}"
    
    def salida_filter(self):
        return f"{self.nombre} en {self.ciudad.nombre}, el {self.fecha.day}"

# Modelo para almacenar generos de forma centralizada    
class Genero(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

# Modelo para almacenar artistas y sus detalles
class Artista(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    generos = models.ManyToManyField(Genero, related_name="artistas", blank=True)
    eventos = models.ManyToManyField(Evento, related_name="artistas", blank=True)
    info = models.TextField(blank=True)

    def __str__(self):
        parts = [
            f"Name: {self.nombre} Info: {self.info}",
        ]
        if self.generos.exists():
            generos_nombres = ", ".join([g.nombre for g in self.generos.all()])
            parts.append(f"Géneros: {generos_nombres}")
        if self.eventos.exists():
            eventos_nombres = ", ".join([g.nombre for g in self.eventos.all()])
            parts.append(f"Géneros: {eventos_nombres}")
        return "\n".join(parts)
    
# Modelo para almacenar detalles de un evento especifico
class EventoDetalle(models.Model):
    evento = models.OneToOneField(Evento, on_delete=models.CASCADE, related_name="detalle")
    horario = models.CharField(max_length=100)
    precio = models.CharField(max_length=100, blank=True, null=True)
    event_info = models.TextField(blank=True, null=True)
    club_info = models.TextField(blank=True, null=True)
    artistas = models.ManyToManyField(Artista, related_name="eventos_detalle", blank=True)
    generos = models.ManyToManyField(Genero, related_name="eventos", blank=True)

    def __str__(self):
        parts = [
            f"Evento: {self.evento.nombre}",
        ]

        if self.horario:
            parts.append(f"Horario: {self.horario}")
        if self.precio:
            parts.append(f"Precio: {self.precio}")
        if self.event_info:
            parts.append(f"Info: {self.event_info}")
        if self.club_info:
            parts.append(f"Club info: {self.club_info}")

        if self.artistas.exists():
            artistas_nombres = ", ".join([a.nombre for a in self.artistas.all()])
            parts.append(f"Artistas: {artistas_nombres}")
        if self.generos.exists():
            generos_nombres = ", ".join([g.nombre for g in self.generos.all()])
            parts.append(f"Géneros: {generos_nombres}")

        return "\n".join(parts)
