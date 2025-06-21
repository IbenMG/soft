import os
from django.conf import settings
from django.db import models
from django.contrib import messages
from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import DocumentoPDF


# Vista principal del gestor
def index_pdf(request):
    return render(request, 'gestor_pdf/index_pdf.html')  # esta es la que se muestra en /pdfs/

# Vista para subir PDF

def agregar_pdf(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        archivo = request.FILES.get('archivo')
        etiquetas = request.POST.get('etiquetas')

        if archivo:
            DocumentoPDF.objects.create(
                nombre=nombre,
                archivo=archivo,
                etiquetas=etiquetas
            )
            messages.success(request, f'Documento "{nombre}" subido correctamente.')
        else:
            messages.error(request, "Debes seleccionar un archivo PDF.")

    return render(request, 'gestor_pdf/agregar_pdf.html')


# Vista para buscar PDF
def buscar_pdf(request):
    query = request.GET.get('q', '')

    if query:
        pdfs = DocumentoPDF.objects.filter(
            models.Q(nombre__icontains=query) | models.Q(etiquetas__icontains=query)
        )
    else:
        pdfs = DocumentoPDF.objects.all()

    # Extraer etiquetas únicas (opcional)
    etiquetas = set()
    for pdf in DocumentoPDF.objects.all():
        for etiqueta in pdf.etiquetas.split(','):
            etiquetas.add(etiqueta.strip())

    context = {
        'pdfs': pdfs,
        'query': query,
        'etiquetas': sorted(etiquetas),
    }

    return render(request, 'gestor_pdf/buscar_pdf.html', context)


def detalle_pdf(request, pdf_id):
    pdf = get_object_or_404(DocumentoPDF, id=pdf_id)
    return render(request, 'gestor_pdfs/detalle_pdf.html', {'documento': pdf})

def modificar_pdf(request, pk):
    if request.session.get('supabase_class') == 'lector':
        return redirect('buscar_pdf')

    pdf = get_object_or_404(DocumentoPDF, pk=pk)

    if request.method == 'POST':
        pdf.nombre = request.POST.get('nombre', pdf.nombre)
        pdf.etiquetas = request.POST.get('etiquetas', pdf.etiquetas)
        if 'archivo' in request.FILES:
            pdf.archivo = request.FILES['archivo']
        pdf.save()

        messages.success(request, "Los cambios fueron guardados correctamente.")
        return redirect('buscar_pdf')

    return render(request, 'gestor_pdf/modificar_pdf.html', {'pdf': pdf})

    return render(request, 'gestor_pdfs/modificar_pdf.html', {'form': form, 'pdf': pdf})

def descargar_pdf(request, pdf_id):
    pdf = get_object_or_404(DocumentoPDF, id=pdf_id)
    ruta_archivo = os.path.join(settings.MEDIA_ROOT, pdf.archivo.name)

    if not os.path.exists(ruta_archivo):
        raise Http404("El archivo solicitado no fue encontrado.")

    return FileResponse(open(ruta_archivo, 'rb'), content_type='application/pdf')

def borrar_pdf(request, pdf_id):
    if request.session.get('supabase_class') == 'lector':
        return redirect('buscar_pdf')

    pdf = get_object_or_404(DocumentoPDF, id=pdf_id)
    
    if request.method == 'POST':
        pdf.delete()
        messages.success(request, f"'{pdf.nombre}' fue eliminado correctamente.")
        return redirect('buscar_pdf')

    return render(request, 'gestor_pdfs/confirmar_borrar.html', {'documento': pdf})

