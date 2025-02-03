from rest_framework import serializers
from .models import ShortenedURL
from django.contrib.auth.models import User

# ✅ Serializador para usuarios (usado en el Dashboard)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# ✅ Serializador para URLs acortadas
class ShortenedURLSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)  # Mostrar info del usuario dueño (solo lectura)

    class Meta:
        model = ShortenedURL
        fields = ['id', 'original_url', 'short_code', 'is_private', 'views', 'owner', 'created_at']
