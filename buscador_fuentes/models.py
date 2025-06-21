from django.db import models

# Modelo Fuente con clave primaria 'id' explícita
class Fuente(models.Model):
    id = models.AutoField(primary_key=True)  # Campo id explícito como clave primaria
    nombre = models.CharField(max_length=255)
    url = models.URLField()
    etiquetas = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

# Modelo Articulo con clave primaria 'id' explícita
class Articulo(models.Model):
    id = models.AutoField(primary_key=True)  # Campo id explícito como clave primaria
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    fuente = models.ForeignKey(Fuente, on_delete=models.CASCADE)  # Relación con el modelo Fuente
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

# Modelo Etiqueta sin campo 'id' explícito, usará el por defecto de Django
class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50)
    articulos = models.ManyToManyField(Articulo)  # Relación Many-to-Many con el modelo Artículo

    def __str__(self):
        return self.nombre

# Create your models here.
