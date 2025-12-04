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
        return f"{self.nombre} - {self.fecha}"

# Modelo para almacenar generos de forma centralizada    
class Genero(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

# Modelo para almacenar artistas y sus detalles
class Artista(models.Model):
    nombre = models.CharField(max_length=200)
    enlace = models.URLField(unique=True)
    generos = models.ManyToManyField(Genero, related_name="artistas", blank=True)
    info = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
    
# Modelo para almacenar detalles de un evento especifico
class EventoDetalle(models.Model):
    evento = models.OneToOneField(Evento, on_delete=models.CASCADE, related_name="detalle")
    horario = models.CharField(max_length=100)
    precio = models.CharField(max_length=100)
    event_info = models.TextField(blank=True, null=True)
    club_info = models.TextField(blank=True, null=True)
    artistas = models.ManyToManyField(Artista, related_name="eventos", blank=True)
    generos = models.ManyToManyField(Genero, related_name="eventos", blank=True)

    def __str__(self):
        return f"Detalles de {self.evento.nombre}"
