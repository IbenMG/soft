import bcrypt
from django.shortcuts import render, redirect
from django.db import connections
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

# Página principal
def admin_index(request):
    user_class = request.session.get('supabase_class', '')

    context = {
        'is_admin': user_class == 'administrador',
        'is_editor': user_class in ['administrador', 'editor'],
        'is_reader': user_class in ['administrador', 'editor', 'lector'],
    }

    return render(request, 'admin.html', context)

class DummyUser:
    def __init__(self, username):
        self.username = username
        self.is_authenticated = True

# Registro con Supabase Auth oficial
def supabase_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        VALID_CLASSES = ['administrador', 'editor', 'lector']
        user_class = request.POST.get('user_class')

        if user_class not in VALID_CLASSES:
            messages.error(request, 'Clase no válida. Debe ser administrador, editor o lector.')
            return render(request, 'register.html')
        # 🔒 Encriptar la contraseña
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        try:
            with connections['remote_supabase'].cursor() as cursor:
                cursor.execute("""
                    INSERT INTO users (username, password, email, class, created_at)
                    VALUES (%s, %s, %s, %s, now())
                """, [username, hashed_password, email, user_class])

            messages.success(request, '¡Cuenta creada exitosamente!')
            return redirect('login')

        except Exception as e:
            messages.error(request, f'Error al crear cuenta: {e}')

    return render(request, 'register.html')
@csrf_exempt
def supabase_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password_input = request.POST.get('password')

        try:
            with connections['remote_supabase'].cursor() as cursor:
                # 👇 Recupera también el campo "class"
                cursor.execute("SELECT password, class FROM users WHERE username = %s", [username])
                row = cursor.fetchone()

            if row:
                stored_hash, user_class = row
                if bcrypt.checkpw(password_input.encode(), stored_hash.encode()):
                    request.session['supabase_user'] = username
                    request.session['supabase_class'] = user_class or 'sin rol'
                    messages.success(request, '¡Sesión iniciada correctamente!')
                    return redirect('home')
                else:
                    messages.error(request, 'Contraseña incorrecta.')
            else:
                messages.error(request, 'Usuario no encontrado.')
        except Exception as e:
            messages.error(request, f'Error en la autenticación: {e}')

    return render(request, 'login.html')

# Logout (borra la sesión)
def supabase_logout(request):
    request.session.flush()
    return redirect('login')

def admin_users(request):
    if request.session.get('supabase_class') != 'administrador':
        return HttpResponseForbidden("Acceso denegado.")

    with connections['remote_supabase'].cursor() as cursor:
        cursor.execute("SELECT id, username, email, class FROM users ORDER BY id")
        rows = cursor.fetchall()

    users = [
        {"id": r[0], "username": r[1], "email": r[2], "class": r[3]}
        for r in rows
    ]

    return render(request, 'admin_users.html', {'users': users})

def home(request):
    return render(request, 'home.html')
