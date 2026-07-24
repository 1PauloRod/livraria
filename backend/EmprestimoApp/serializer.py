from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Emprestimo
from LivroApp.serializer import LivroSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ["id", "name", "last_name", "email"]


class EmprestimoSerializer(serializers.ModelSerializer):

    dias_atraso = serializers.ReadOnlyField()
    multa = serializers.ReadOnlyField()
    livro = LivroSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Emprestimo
        fields = "__all__"