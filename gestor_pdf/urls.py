from django.urls import path, include 
from . import views
from .views import buscar_pdf
from .views import (
    index_pdf,
    agregar_pdf,
    buscar_pdf,
    detalle_pdf,
    modificar_pdf,
    descargar_pdf,
    borrar_pdf,
)


urlpatterns = [
    path('', index_pdf, name='index_pdfs'),
    path('agregar/', agregar_pdf, name='agregar_pdf'),
    path('buscar/', buscar_pdf, name='buscar_pdf'),
    path('<int:pdf_id>/', detalle_pdf, name='detalle_pdf'),
    path('descargar/<int:pdf_id>/', descargar_pdf, name='descargar_pdf'),
    path('modificar/<int:pk>/', modificar_pdf, name='modificar_pdf'),
    path('borrar/<int:pdf_id>/', borrar_pdf, name='confirmar_borrar'),
]
