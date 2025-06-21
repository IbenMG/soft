from django.db import models


class UsuarioSupabase(models.Model):
    id = models.BigAutoField(primary_key=True)
    creado_en = models.DateTimeField()
    nombre_usuario = models.CharField(max_length=255)
    contrasena = models.CharField(max_length=255)
    rol = models.CharField(max_length=255, db_column='class') 
    correo = models.EmailField(null=True, db_column='email')

    class Meta:
        db_table = 'users'
        managed = False 

    def __str__(self):
        return self.nombre_usuario


class Boletin(models.Model):
    titulo = models.CharField("Título", max_length=200)
    contenido_html = models.TextField("Contenido HTML")
    imagen_destacada = models.ImageField(
        "Imagen", upload_to='boletines/', blank=True, null=True
    )
    creado = models.DateTimeField("Fecha de creación", auto_now_add=True)
    modificado = models.DateTimeField("Última modificación", auto_now=True)
    esta_publicado = models.BooleanField("Publicado", default=False)
    es_plantilla = models.BooleanField("Es plantilla", default=False)

    class Meta:
        verbose_name = "Boletín"
        verbose_name_plural = "Boletines"

    def __str__(self):
        return self.titulo


class PlantillaHTML(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    html = models.TextField("Código HTML")

    class Meta:
        verbose_name = "Plantilla"
        verbose_name_plural = "Plantillas"

    def __str__(self):
        return self.nombre


# Create your models here.
