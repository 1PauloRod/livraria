from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Livro
from .serializer import LivroSerializer
from EmprestimoApp.models import Emprestimo
from django.utils import timezone

class ListaLivrosView(APIView):

    def get(self, request):
        
        q = request.query_params.get("q", "") 

        if q:
            livros = Livro.objects.filter(
                titulo__icontains=q
            ) | Livro.objects.filter(
                autor__icontains=q
            )
        else:
            livros = Livro.objects.all()
        
        serializer = LivroSerializer(livros, many=True)
        return Response(serializer.data)
    

class DeletarLivro(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, livro_id):
        
        if not request.user.is_superuser:
            return Response({"detail": "Permissão negada."}, status=403)
        
        try:
            livro = Livro.objects.get(id=livro_id)
        
        except Livro.DoesNotExist:
            return Response({"detail": "Livro não encontrado."}, status=404)
        
        emprestimo_ativo = Emprestimo.objects.filter(
                                                    livro=livro, 
                                                     user=request.user
                                                     )
        
        if emprestimo_ativo:
            emprestimo_ativo.data_devolucao = timezone.now()
            emprestimo_ativo.save()
        
        livro.delete()

        return Response({"detail": "Livro excluído com sucesso."}, status=200)



class AdicionarLivroView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):

        if not request.user.is_superuser:
            return Response({"detail": "Apenas admin podem adicionar livros."}, 
                            status=403)

        serializer = LivroSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Livro adicionado com sucesso!", 
                "livro": serializer.data
            }, status=201)
        
        return Response(serializer.error, status=400)

class AtualizarLivroView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, livro_id):

        if not request.user.is_superuser:
            return Response({"detail": "Apenas admin pode editar"}, status=403)
        
        try:
            livro = Livro.objects.get(id=livro_id)
        except Livro.DoesNotExist:
            return Response({"detail": "Livro não encontrado"}, status=404)
        
        serializer = LivroSerializer(livro, data=request.data, partial=False)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Livro atualizado com sucesso!", 
                            "livro": serializer.data}, status=201)
        return Response(serializer.errors, status=404)
        
    




        
        