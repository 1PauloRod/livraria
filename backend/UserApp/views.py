from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .models import User
from EmprestimoApp.models import Emprestimo

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=201)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    permission_classes = [AllowAny] 
    authentication_classes = []

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
    authentication_classes = [TokenAuthentication] 

    def post(self, request):
        request.auth.delete()

        return Response({"message": "Logout realizado com sucesso"})
    

def is_admin(user):
    return user.is_superuser

class MeView(APIView):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

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
    authentication_classes = [TokenAuthentication]

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
    authentication_classes = [TokenAuthentication]

    def get(self, request):

        user = request.user
        
        if not is_admin(user):
            return Response({"detail": "Apenas admin podem adicionar livros."}, 
                            status=403) 
            
        
        q = request.query_params.get("q", "")

        if q:
            usuarios = User.objects.filter(
                email__icontains=q
                ) | User.objects.filter(
                    name__icontains = q
                ) | User.objects.filter(
                    last_name__icontains = q
                )
        else:
            usuarios = User.objects.filter(is_superuser=False)
        
        serializer = UserSerializer(usuarios, many=True)
        
        return Response(serializer.data)




        


    

