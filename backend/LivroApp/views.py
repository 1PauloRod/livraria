from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Livro
from .services import lista_livro, deleta_livro, busca_livro
from .permissions import isAdmin
from .serializer import LivroSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse


class BuscaLivroOpenLibraryView(APIView):

    permission_classes = [IsAuthenticated, isAdmin]

    def get(self, request):
        
        q = request.query_params.get("q") 
        
        print("q =", q)
        
        livros = busca_livro(q)
        
        return Response(livros)
    
    
class ImportarLivroView(APIView):
    
    permission_classes = [IsAuthenticated, isAdmin]
    
    def post(self, request):
        
        data = request.data
        
        livro, created = Livro.objects.get_or_create(
        obra_id=data["obra_id"],
        defaults={
        "titulo": data["titulo"],
        "autor": data["autores"],
        "ano": data["ano"],
        "editora": data["editora"],
            }
        )               
        
        return Response({
            "created": created,
            "livro": livro.titulo
        })
        
        
    
class ListaLivrosView(APIView):
    
    permission_classes = [IsAuthenticated]
        
    @extend_schema(
        summary="Listar livros",
        description="""
        Retorna uma lista de livros cadastrados.

        É possível filtrar os resultados utilizando o parâmetro `q`,
        que busca livros por termo informado.
        """,
        parameters=[
            OpenApiParameter(
                name="q",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Termo de busca para filtrar livros"
            )
        ],
        responses={
            200: LivroSerializer(many=True),
        },
        tags=["Livros"]
    )

    def get(self, request):
        
        q = request.query_params.get("q", "") 

        livros = lista_livro(q)  
        
        serializer = LivroSerializer(livros, many=True)
        
        return Response(serializer.data)
    

class DeletarLivro(APIView):

    permission_classes = [IsAuthenticated, isAdmin]
    
    @extend_schema(
        summary="Excluir livro",
        description="Remove um livro do sistema pelo ID.",
        parameters=[
            OpenApiParameter(
                name="livro_id",
                type=int,
                location=OpenApiParameter.PATH,
                description="ID do livro a ser removido"
            )
        ],
        responses={
            200: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "Dom Casmurro removido."
                    }
                }
            },
            404: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "Livro não encontrado."
                    }
                }
            },
            401: None,
            403: None,
        },
        tags=["Livros"],
    )

    def delete(self, request, livro_id): 
        try:
            livro = deleta_livro(livro_id, request.user)
        
        except Livro.DoesNotExist:
            return Response({"detail": "Livro não encontrado."}, status=404)
        
        return Response({"detail": f"{livro.titulo} removido."}, status=200)
        


class AdicionarLivroView(APIView):
    
    permission_classes = [IsAuthenticated, isAdmin]
    
    @extend_schema(
        summary="Adicionar livro",
        description="Cadastra um novo livro no sistema.",
        request=LivroSerializer,
        responses={
            201: LivroSerializer,
            400: None,
            401: None,
            403: None,
        },
        tags=["Livros"],
    )

    def post(self, request):

        try:
            serializer = LivroSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
           
            return Response({"message": "Livro adicionado com sucesso!", 
                           "livro": serializer.data
                           }, status=201)
        
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=400
            )

class AtualizarLivroView(APIView):

    permission_classes = [IsAuthenticated, isAdmin]
    
    @extend_schema(
        summary="Atualizar livro",
        description="Atualiza parcialmente os dados de um livro pelo ID.",
        parameters=[
            OpenApiParameter(
                name="livro_id",
                type=int,
                location=OpenApiParameter.PATH,
                description="ID do livro a ser atualizado"
            )
        ],
        request=LivroSerializer,
        responses={
            202: LivroSerializer,
            404: None,
            401: None,
            403: None,
        },
        tags=["Livros"],
    )

    def post(self, request, livro_id):

        try:
            livro = Livro.objects.get(id=livro_id)

            serializer = LivroSerializer(
                livro,
                data=request.data,
                partial=True
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "message": "Livro atualizado com sucesso!",
                "livro": serializer.data
            }, status=202)

        except Livro.DoesNotExist:

            return Response({
                "detail": "Livro não encontrado."
            }, status=404)
             
        
    




        
        