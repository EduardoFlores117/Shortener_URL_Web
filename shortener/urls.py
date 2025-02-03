from django.urls import path
from .views import (
    login_view, register_view, logout_view, RedirectURLView,
    admin_dashboard, user_dashboard, shorten_url_view, delete_url,register_template_view, bulk_shorten_urls
)

urlpatterns = [
    # ✅ Autenticación
    path('auth/login/', login_view, name='login'),
    path('auth/register/', register_view, name='register'),
    path('auth/registers/', register_template_view, name='register_template'),
    path('auth/logout/', logout_view, name='logout'),

    # ✅ Dashboards
    path('dashboard/admin/', admin_dashboard, name='dashboard_admin'),
    path('dashboard/user/', user_dashboard, name='dashboard_user'),

    # ✅ Formulario para acortar URLs
    path('shorten/', shorten_url_view, name='shorten_url'),

    # ✅ Redirección de URLs acortadas
    path('r/<str:short_code>/', RedirectURLView.as_view(), name='redirect_url'),

    # ✅ Eliminación de URLs
    path('urls/delete/<int:url_id>/', delete_url, name='delete_url'),
    
    path('shorten/bulk/', bulk_shorten_urls, name='bulk_shorten'),
]
