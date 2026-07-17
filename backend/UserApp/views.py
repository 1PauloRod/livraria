from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .models import User
from EmprestimoApp.models import Emprestimo
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .pagination import DefaultPagination

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    @extend_schema(
        summary="Registrar usuário",
        description="Cria um novo usuário e retorna um token de autenticação.",
        request=RegisterSerializer,
        responses={
            201: {
                "type": "object",
                "properties": {
                    "token": {
                        "type": "string",
                        "example": "abc123tokenxyz"
                    }
                }
            },
            400: RegisterSerializer,
        },
        tags=["Autenticação"],
    )

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=201)
        
        print("ERRORS:", serializer.errors)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    permission_classes = [AllowAny] 
    authentication_classes = []
    
    @extend_schema(
        summary="Login do usuário",
        description="Autentica o usuário via email e senha e retorna um token.",
        request={
            "type": "object",
            "properties": {
                "email": {"type": "string", "example": "user@email.com"},
                "password": {"type": "string", "example": "123456"},
            },
            "required": ["email", "password"],
        },
        responses={
            200: {
                "type": "object",
                "properties": {
                    "token": {
                        "type": "string",
                        "example": "abc123token"
                    }
                }
            },
            400: {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            }
        },
        tags=["Autenticação"],
    )

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password") 

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Email não encontrado"}, status=400)
        
        user = authenticate(email=user_obj.email, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Senha incorreta"}, status=400)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Logout do usuário",
        description="Remove o token de autenticação do usuário logado.",
        request=None,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "Logout realizado com sucesso"
                    }
                }
            },
            401: None,
        },
        tags=["Autenticação"],
    )

    def post(self, request):
        request.auth.delete()

        return Response({"message": "Logout realizado com sucesso"})
    

def is_admin(user):
    return user.is_superuser

class MeView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Dados do usuário logado",
        description="Retorna os dados do usuário autenticado no sistema.",
        request=None,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "name": {"type": "string", "example": "João"},
                    "last_name": {"type": "string", "example": "Silva"},
                    "email": {"type": "string", "example": "joao@email.com"},
                    "bibliotecario": {"type": "boolean", "example": True},
                }
            },
            401: None,
        },
        tags=["Usuário"],
    )
    
    
    def get(self, request):
        user = request.user

        if is_admin(user):
            return Response({
                "id": user.id, 
                "name": user.name, 
                "last_name": user.last_name, 
                "email": user.email, 
                "bibliotecario": True
            })
        
        return Response({
                "id": user.id, 
                "name": user.name, 
                "last_name": user.last_name, 
                "email": user.email, 
                "bibliotecario": False
            })


class DeletaUsuario(APIView):

    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Deletar usuário",
        description="Remove um usuário do sistema. Apenas administradores podem executar esta ação.",
        parameters=[
            OpenApiParameter(
                name="user_id",
                type=int,
                location=OpenApiParameter.PATH,
                description="ID do usuário que será deletado"
            )
        ],
        responses={
            200: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "Usuário excluído com sucesso."
                    }
                }
            },
            403: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "Apenas admin podem deletar usuários."
                    }
                }
            },
            400: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "Usuário tem empréstimos ativos."
                    }
                }
            },
        },
        tags=["Usuários"],
    )

    def delete(self, request, user_id):
        
        user = request.user
        
        if not is_admin(user):
            return Response({"detail": "Apenas admin podem deletar usuários."}, 
                            status=403)
        
        usuario_deletar = User.objects.get(id=user_id)
        emprestimos_on = Emprestimo.objects.filter(user=usuario_deletar).exists()
        if emprestimos_on:
            return Response({"detail": "Usuário tem empréstimos ativos."}, 
                            status=402)

        usuario_deletar.delete()

        return Response({"detail": "Usuário excluído com sucesso."}, status=200) 

class ListaUsuarios(APIView):

    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Listar usuários",
        description="Retorna todos os usuários (exceto admin/superuser). Apenas administradores podem acessar.",
        parameters=[
            OpenApiParameter(
                name="q",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filtro por email, nome ou sobrenome"
            )
        ],
        responses={
            200: UserSerializer(many=True),
            403: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "Apenas admin podem adicionar livros."
                    }
                }
            }
        },
        tags=["Usuários"],
    )

    def get(self, request):

        user = request.user
        
        if not is_admin(user):
            return Response({"detail": "Apenas admin podem adicionar livros."}, 
                            status=403) 
            
        
        q = request.query_params.get("q", "")

        if q:
            usuarios = User.objects.filter(
                email__icontains=q, is_superuser=False
                ) | User.objects.filter(
                    name__icontains = q, is_superuser=False
                ) | User.objects.filter(
                    last_name__icontains = q, is_superuser=False
                )
        else:
            usuarios = User.objects.filter(is_superuser=False)
            
        paginator = DefaultPagination()
        
        page = paginator.paginate_queryset(
            usuarios, 
            request
        )
        
        serializer = UserSerializer(page, many=True)
        
        return paginator.get_paginated_response(serializer.data)




        


    

