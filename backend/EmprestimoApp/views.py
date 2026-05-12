from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from LivroApp.models import Livro
from .models import Emprestimo
from UserApp.models import User
from .serializer import EmprestimoSerializer
from  django.utils import timezone


class ListaEmprestimo(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        q = request.query_params.get("q", "")
        
        if q:
            livros = Livro.objects.filter(
                titulo__icontains=q
            ) | Livro.objects.filter(
                autor__icontains=q
            )
            
            emprestimos = Emprestimo.objects.filter(
                user = request.user,
                Livro=livros
            )
        else:
            emprestimos = Emprestimo.objects.filter(user = request.user)
        
        serializer = EmprestimoSerializer(emprestimos, many=True) 
        return Response(serializer.data)


class ListaTodosEmprestimosView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        if not request.user.is_superuser:
            return Response({"detail": "Apenas admin podem adicionar livros."}, 
                            status=403) 


        q = request.query_params.get("q", "")

        if q:
            usuario = User.objects.filter(
                email__icontains = q
            )
            emprestimos = User.objects.filter(
                user = usuario
            )

        emprestimos = Emprestimo.objects.all()

        serializer = EmprestimoSerializer(emprestimos, many=True)

        return Response(serializer.data)

class AlugarLivroView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request, livro_id):
        try:
            livro = Livro.objects.get(id=livro_id) 
        except Livro.DoesNotExist:
            return Response({"error": "Livro não existe."}, status=404)

        if not livro.disponivel:
            return Response({"error": "Livro indisponível"}, status=400)
         
        emprestimo = Emprestimo.objects.create(
            livro=livro, 
            user = request.user
        )

        livro.disponivel = False
        livro.save()

        
        serializer = EmprestimoSerializer(emprestimo)

        return Response({
            "mensagem": "Livro alugado com sucesso!",
            "data": serializer.data}, status=201)
    

class DevolverLivro(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request, emprestimo_id):

        if not request.user.is_superuser:
            return Response({"detail": "Permissão negada."}, status=403)
        
        try:
            emprestimo = Emprestimo.objects.get(id=emprestimo_id)
        except Emprestimo.DoesNotExist:
            return Response({"error": "Empréstimo não encontrado."}, status=404)
        

        if emprestimo.data_devolucao:
            return Response({"erro": "Livro já foi devolvido."}, status=400)
        
        emprestimo.data_devolucao = timezone.now()
        emprestimo.save()

        emprestimo.livro.disponivel = True
        emprestimo.livro.save()

        return Response({
            "mensagem": "Livro devolvido com sucesso.", 
            "data_devolucao": emprestimo.data_devolucao
        }, status=201)
