from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


from .views import (
    admin_index,
    supabase_register,
    supabase_login,
    supabase_logout,
    admin_users,
)

urlpatterns = [
    path('', admin_index, name='admin_index'),
    path('register/', supabase_register, name='supabase_register'),
    path('login/', supabase_login, name='login'),
    path('logout/', supabase_logout, name='logout'),
    path('admin/users/', admin_users, name='admin_users'),
    path('pdfs/', include('gestor_pdf.urls')),  # ✅ solo una vez
    path('admin/', admin.site.urls),  # ✅ esto habilita el panel de Django
    path('fuentes/', include('buscador_fuentes.urls')),
    path('editor/', include('editor.urls')),
    path('', views.home, name='home'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

