from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from LivroApp.models import Livro
from .models import Emprestimo
from .serializer import EmprestimoSerializer
from .permissions import isAdmin, isNotAdmin
from .services import lista_emprestimo, lista_todos_emprestimos, alugar_livro, devolver_livro
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse


class ListaEmprestimo(APIView):
    
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Listar emprestimos",
        description="""
        Retorna uma lista de emprestimos cadastrados.

        É possível filtrar os resultados utilizando o parâmetro `q`,
        que busca emprestimos por termo informado.
        """,
        parameters=[
            OpenApiParameter(
                name="q",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Termo de busca para filtrar emprestimos"
            )
        ],
        responses={
            200: EmprestimoSerializer(many=True),
            
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
        },
        
        tags=["Emprestimos"]
    )

    def get(self, request):

        q = request.query_params.get("q", "")
        
        emprestimo = lista_emprestimo(q, request.user)
        
        serializer = EmprestimoSerializer(emprestimo, many=True)
        
        return Response(serializer.data)
        

class ListaTodosEmprestimosView(APIView):

    permission_classes = [IsAuthenticated, isAdmin]

class ListaTodosEmprestimosView(APIView):

    permission_classes = [IsAuthenticated, isAdmin]

    @extend_schema(
        summary="Listar todos os empréstimos",
        description="""
        Retorna a lista de todos os empréstimos cadastrados.

        É possível filtrar os resultados utilizando o parâmetro `q`,
        que busca empréstimos conforme o critério definido pela regra
        de negócio.
        """,
        parameters=[
            OpenApiParameter(
                name="q",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Termo utilizado para filtrar empréstimos"
            )
        ],
        responses={
            200: OpenApiResponse(
                description="Lista de empréstimos retornada com sucesso"
            ),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
            403: OpenApiResponse(
                description="Usuário sem permissão de administrador"
            ),
        },
        tags=["Empréstimos"]
    )
    def get(self, request):

        q = request.query_params.get("q", "")

        emprestimos = lista_todos_emprestimos(q)

        return Response(emprestimos)

    def get(self, request):

        q = request.query_params.get("q", "")

        emprestimos = lista_todos_emprestimos(q)
        
        serializer = EmprestimoSerializer(emprestimos, many=True)
        
        return Response(serializer.data)
        

class AlugarLivroView(APIView):

    permission_classes = [IsAuthenticated, isNotAdmin]

    @extend_schema(
        summary="Alugar livro",
        description="""
        Realiza o aluguel de um livro para o usuário autenticado.

        O sistema verifica se o livro existe e se está disponível
        para empréstimo antes de efetuar a operação.
        """,
        parameters=[
            OpenApiParameter(
                name="livro_id",
                type=int,
                location=OpenApiParameter.PATH,
                required=True,
                description="ID do livro a ser alugado"
            )
        ],
        responses={
            201: OpenApiResponse(
                description="Livro alugado com sucesso"
            ),
            400: OpenApiResponse(
                description="Livro indisponível ou regra de negócio violada"
            ),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
            404: OpenApiResponse(
                description="Livro não encontrado"
            ),
        },
        tags=["Empréstimos"]
    )
    def post(self, request, livro_id):
        try:

            emprestimo = alugar_livro(livro_id, request.user)

            serializer = EmprestimoSerializer(emprestimo)

            return Response({
                "mensagem": "Livro alugado com sucesso!",
                "data": serializer.data
            }, status=201)

        except Livro.DoesNotExist:

            return Response({
                "error": "Livro não existe."
            }, status=404)

        except ValueError as e:

            return Response({
                "error": str(e)
            }, status=400)
    


class DevolverLivro(APIView):

    permission_classes = [IsAuthenticated, isAdmin]

    @extend_schema(
        summary="Devolver livro",
        description="""
        Realiza a devolução de um livro associado a um empréstimo.

        Apenas administradores podem executar esta operação.
        A data de devolução é registrada automaticamente.
        """,
        parameters=[
            OpenApiParameter(
                name="emprestimo_id",
                type=int,
                location=OpenApiParameter.PATH,
                required=True,
                description="ID do empréstimo a ser finalizado"
            )
        ],
        responses={
            201: OpenApiResponse(
                description="Livro devolvido com sucesso"
            ),
            400: OpenApiResponse(
                description="Erro de validação ou regra de negócio"
            ),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
            403: OpenApiResponse(
                description="Usuário sem permissão de administrador"
            ),
            404: OpenApiResponse(
                description="Empréstimo não encontrado"
            ),
        },
        tags=["Empréstimos"]
    )
    def post(self, request, emprestimo_id):

        try:
            emprestimo = devolver_livro(emprestimo_id)

            return Response({
                "mensagem": "Livro devolvido com sucesso.",
                "data_devolucao": emprestimo.data_devolucao
            }, status=201)

        except Emprestimo.DoesNotExist:
            return Response({
                "error": "Empréstimo não encontrado."
            }, status=404)

        except ValueError as e:
            return Response({
                "error": str(e)
            }, status=400)

       
