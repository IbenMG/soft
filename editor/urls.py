from django.urls import path
from . import views

app_name = 'editor'

urlpatterns = [
    path('', views.listar_boletines, name='lista'),
    path('crear/', views.formulario_boletin, name='crear'),
    path('editar/<int:pk>/', views.formulario_boletin, name='editar_boletin'),
    path('eliminar/<int:pk>/', views.eliminar_boletin, name='eliminar_boletin'),
    path('publicar/<int:pk>/', views.publicar_boletin, name='publicar_boletin'),
    path('preview/<int:pk>/', views.vista_previa_boletin, name='preview'),
    path('plantilla/usar/<int:pk>/', views.usar_plantilla_boletin, name='usar_plantilla'),
    path('tinymce/templates/', views.tinymce_templates, name='tinymce_templates'),
    path('imagenes/subir/', views.upload_image, name='upload_image'),


]
