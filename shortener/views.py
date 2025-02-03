from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import random, string, json
from rest_framework.views import APIView  # ✅ Se corrige la importación faltante
from .models import ShortenedURL
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
import tempfile
from django.core.files.storage import default_storage
from django.http import JsonResponse, FileResponse
import os
from django.conf import settings

# ✅ Generar código corto para la URL
def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# ✅ Redirección a Login
def home_redirect(request):
    return redirect('/auth/login/')

# ✅ Vista: Inicio de sesión
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=email, password=password)

        if user:
            login(request, user)
            return redirect("/dashboard/admin/" if user.is_superuser else "/dashboard/user/")
        else:
            return JsonResponse({"error": "Usuario o contraseña incorrectos"}, status=400)

    return render(request, "login.html")

# ✅ Vista: Registro de usuario (Formulario HTML)
def register_template_view(request):
    return render(request, "registers.html")

# ✅ Vista: Cerrar sesión
def logout_view(request):
    logout(request)
    return redirect("/auth/login/")

# ✅ Vista: Acortar URL (Usuario autenticado)
@login_required
def shorten_url_view(request):
    if request.method == "POST":
        original_url = request.POST.get("original_url", "").strip()

        if not original_url:
            return JsonResponse({"error": "Debes ingresar una URL válida."}, status=400)

        # Guardar la URL en la base de datos
        short_url = ShortenedURL.objects.create(
            original_url=original_url,
            owner=request.user,
            short_code=generate_short_code()
        )

        # Obtener lista actualizada de URLs
        urls = ShortenedURL.objects.filter(owner=request.user).order_by('-id')
        urls_data = [
            {
                "id": url.id,
                "original_url": url.original_url,
                "short_url": url.get_short_url(),
                "views": url.views
            }
            for url in urls
        ]

        return JsonResponse({
            "message": "URL acortada exitosamente",
            "urls": urls_data
        })

    return render(request, "dashboard_user.html")


# ✅ Vista: Eliminar URL (Solo dueño o superusuario)
@login_required
def delete_url(request, url_id):
    url = get_object_or_404(ShortenedURL, id=url_id)

    if request.user == url.owner or request.user.is_superuser:
        url.delete()
        return JsonResponse({"message": "URL eliminada correctamente"}, status=200)
    else:
        return JsonResponse({"error": "No tienes permisos para eliminar esta URL"}, status=403)
    
# ✅ Vista API: Registro de usuario
@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({"error": "Todos los campos son obligatorios"}, status=400)

            if User.objects.filter(username=email).exists():
                return JsonResponse({"error": "El usuario ya existe"}, status=400)

            user = User.objects.create_user(username=email, email=email, password=password)
            login(request, user)

            return JsonResponse({"message": "Registro exitoso"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato JSON inválido"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)

# ✅ Vista: Dashboard Usuario
@login_required
def user_dashboard(request):
    urls = ShortenedURL.objects.filter(owner=request.user)
    paginator = Paginator(urls, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "dashboard_user.html", {"page_obj": page_obj})

# ✅ Vista: Dashboard Administrador
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('/dashboard/user/')
    
    # 🔹 Obtener el ID del usuario seleccionado en el filtro
    selected_user_id = request.GET.get("user_id")

    # 🔹 Si no hay usuario seleccionado, obtener todas las URLs
    if selected_user_id and selected_user_id != "all":
        urls = ShortenedURL.objects.filter(owner_id=selected_user_id).order_by("-id")
    else:
        urls = ShortenedURL.objects.all().order_by("-id")

    # 🔹 Aplicar paginación de 15 registros por página
    paginator = Paginator(urls, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # 🔹 Retornar datos en JSON si la solicitud proviene de JavaScript
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        urls_data = [
            {
                "id": url.id,
                "original_url": url.original_url,
                "short_url": url.get_short_url(),
                "views": url.views
            }
            for url in page_obj
        ]
        pagination_data = {
            "current_page": page_obj.number,
            "total_pages": paginator.num_pages,
            "has_previous": page_obj.has_previous(),
            "has_next": page_obj.has_next(),
            "previous_page": page_obj.previous_page_number() if page_obj.has_previous() else None,
            "next_page": page_obj.next_page_number() if page_obj.has_next() else None,
        }
        return JsonResponse({"urls": urls_data, "pagination": pagination_data})

    # 🔹 Obtener la lista de usuarios para el filtro en el template
    users = User.objects.all()

    return render(request, "dashboard_admin.html", {
        "page_obj": page_obj,
        "users": users,
        "selected_user_id": selected_user_id or "all"
    })
    
@login_required
def user_dashboard(request):
    urls = ShortenedURL.objects.filter(owner=request.user).order_by('-id')  # Orden descendente
    paginator = Paginator(urls, 10)  # 10 registros por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "dashboard_user.html", {"page_obj": page_obj})

    
@csrf_exempt
@login_required
def bulk_shorten_urls(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        temp_file_path = default_storage.save(f"temp/{file.name}", file)

        shortened_urls = []
        with default_storage.open(temp_file_path, "r") as f:
            for line in f:
                original_url = line.strip()
                if original_url:
                    short_url = ShortenedURL.objects.create(
                        original_url=original_url,
                        owner=request.user,
                        short_code=generate_short_code()
                    )
                    shortened_urls.append(f"{original_url} -> {short_url.get_short_url()}")

        # Crear archivo de salida
        output_file_path = os.path.join(settings.MEDIA_ROOT, "shortened_urls.txt")
        with open(output_file_path, "w") as out_file:
            out_file.write("\n".join(shortened_urls))

        return JsonResponse({"file_url": f"/shortened-files/shortened_urls.txt"})

    return JsonResponse({"error": "No se pudo procesar el archivo"}, status=400)


# ✅ API: Redirección de URLs acortadas
class RedirectURLView(APIView):  # ✅ Ahora APIView está definido correctamente
    def get(self, request, short_code):
        url_instance = get_object_or_404(ShortenedURL, short_code=short_code)

        if url_instance.is_private and not request.user.is_authenticated:
            return JsonResponse({"error": "Esta URL es privada. Debes iniciar sesión."}, status=401)

        url_instance.views += 1
        url_instance.save()

        return redirect(url_instance.original_url)   
