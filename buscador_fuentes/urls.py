from django.urls import path
from . import views

urlpatterns = [
    path('index_fuentes/', views.index_fuentes, name='index_fuentes'), # Ruta para la vista principal
    path('agregar_fuentes/', views.agregar_fuentes, name='agregar_fuentes'),
    path('buscar_fuentes/', views.buscar_fuentes, name='buscar_fuentes'),
    path("buscar-modificar/", views.buscar_para_modificar, name="buscar_para_modificar"),
    path("buscar-borrar/", views.buscar_para_borrar, name="buscar_para_borrar"),
    path('modificar_fuentes/<int:fuente_id>/', views.modificar_fuentes, name='modificar_fuentes'),
    path('borrar_fuentes/<int:fuente_id>/', views.borrar_fuentes, name='borrar_fuentes'),
    path('', views.vistas_fuentes, name='vistas_fuentes'),
]