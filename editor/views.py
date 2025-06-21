from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone, text
from django.conf import settings
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from io import BytesIO
from django.http import JsonResponse
import os
from django.core.files.storage import default_storage
from django.contrib import messages

from .models import Boletin
from .forms import BoletinForm
from gestor_pdf.models import DocumentoPDF
from weasyprint import HTML


def listar_boletines(request):
    if request.session.get('supabase_class') not in ['editor', 'administrador']:
        return HttpResponseForbidden("Acceso denegado.")
    boletines = Boletin.objects.all().order_by('-creado')

    return render(request, 'editor/lista_boletin.html', {'boletines': boletines})


def ver_boletin(request, pk):
    boletin = get_object_or_404(Boletin, pk=pk)
    return render(request, 'editor/boletin_detalles.html', {'boletin': boletin})


def formulario_boletin(request, pk=None):
    if pk:
        boletin = get_object_or_404(Boletin, pk=pk)
    else:
        boletin = None

    if request.method == 'POST':
        form = BoletinForm(request.POST, request.FILES, instance=boletin)
        if form.is_valid():
            nuevo_boletin = form.save()
            messages.success(request, 'Boletín guardado correctamente.')
            return redirect('editor:editar_boletin', pk=nuevo_boletin.pk)
    else:
        form = BoletinForm(instance=boletin)

    return render(request, 'editor/forma_boletin.html', {
        'form': form,
        'boletin': boletin,
    })


def eliminar_boletin(request, pk):
    boletin = get_object_or_404(Boletin, pk=pk)
    
    if request.method == 'POST':
        boletin.delete()
        messages.success(request, 'Boletín eliminado correctamente.')
        return redirect('editor:lista')
    
    return render(request, 'editor/confirmar_eliminar.html', {'boletin': boletin})


def usar_plantilla_boletin(request, pk):
    base = get_object_or_404(Boletin, pk=pk, es_plantilla=True)
    nuevo = Boletin.objects.create(
        titulo=f"Nuevo boletín desde plantilla: {base.titulo}",
        contenido=base.contenido,
        imagen=base.imagen,
        publicado=False,
        es_plantilla=False,
        fecha_creacion=timezone.now()
    )
    return redirect('editar_boletin', pk=nuevo.pk)


def vista_previa_boletin(request, pk):
    boletin = get_object_or_404(Boletin, pk=pk)
    return render(request, 'editor/pboletin.html', {'boletin': boletin, 'preview': True})


@csrf_exempt
def subir_imagen(request):
    if request.method == 'POST':
        imagen = request.FILES.get('file')
        if not imagen:
            return JsonResponse({'error': 'Archivo no proporcionado'}, status=400)

        ruta = os.path.join('uploads', imagen.name)
        ruta_completa = os.path.join(settings.MEDIA_ROOT, ruta)

        os.makedirs(os.path.dirname(ruta_completa), exist_ok=True)
        with open(ruta_completa, 'wb+') as archivo:
            for chunk in imagen.chunks():
                archivo.write(chunk)

        return JsonResponse({'location': settings.MEDIA_URL + ruta})




def exportar_boletin_a_pdf(boletin):
    html = render_to_string('editor/boletin_pdf.html', {'boletin': boletin})
    buffer = BytesIO()
    HTML(string=html).write_pdf(buffer)
    return ContentFile(buffer.getvalue(), name=f"boletin_{boletin.pk}.pdf")


def publicar_boletin(request, pk):
    boletin = get_object_or_404(Boletin, pk=pk)
    if not boletin.contenido.strip():
        messages.error(request, "El boletín no tiene contenido para publicar.")
        return redirect('editar_boletin', pk=pk)

    boletin.publicado = True
    boletin.fecha_creacion = timezone.now()
    boletin.save()

    pdf = exportar_boletin_a_pdf(boletin)
    DocumentoPDF.objects.create(
        nombre=boletin.titulo,
        archivo=pdf,
        etiquetas=text.slugify(boletin.titulo)
    )

    messages.success(request, "Boletín publicado y PDF generado correctamente.")
    return redirect('editar_boletin', pk=pk)

# Create your views here.
def tinymce_templates(request):
    templates = [
        {
            "title": "Plantilla básica",
            "description": "Ejemplo de estructura para boletines",
            "content": "<h2>Título</h2><p>Contenido de ejemplo...</p>"
        }
    ]
    return JsonResponse(templates, safe=False)

def upload_image(request):
    """Maneja la carga de imágenes desde TinyMCE"""
    if request.method == 'POST':
        image = request.FILES.get('file')
        if not image:
            return JsonResponse({'error': 'No se recibió archivo'}, status=400)

        path = default_storage.save(os.path.join('boletines', image.name), image)
        image_url = f"{settings.MEDIA_URL}{path}"
        return JsonResponse({'location': image_url})

    return JsonResponse({'error': 'Método no permitido'}, status=405)
# Create your views here.
def editar_boletin(request, pk):
    if request.session.get('supabase_class') != 'editor':
        return HttpResponseForbidden("Acceso no permitido.")

    boletin = get_object_or_404(Boletin, pk=pk)

    if request.method == 'POST':
        form = BoletinForm(request.POST, instance=boletin)
        if form.is_valid():
            form.save()
            return redirect('lista_boletines')
        else:
            print("Errores del formulario:", form.errors)