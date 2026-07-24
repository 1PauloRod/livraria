from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Livro
from .services import lista_livro, deleta_livro, busca_livro, importar_livro
from .permissions import isAdmin
from .serializer import LivroSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from .exceptions import BookNotFoundError, ActivateBookLoan
from rest_framework.exceptions import ValidationError
from .pagination import DefaultPagination
from django.core.cache import cache

class BuscaLivroOpenLibraryView(APIView):

    permission_classes = [IsAuthenticated, isAdmin]
    
    @extend_schema(
    summary="Buscar livros na OpenLibrary",
    description="""
    Realiza uma busca de livros na API da OpenLibrary.

    Utilize o parâmetro `q` para informar o termo desejado (título, autor ou ISBN).
    Retorna uma lista de livros encontrados, mas **não os adiciona ao banco de dados**.
    """,
    parameters=[
        OpenApiParameter(
            name="q",
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description="Termo utilizado na busca da OpenLibrary"
        )
    ],
    responses={
        200: OpenApiResponse(
            description="Lista de livros encontrados."
        ),
        400: OpenApiResponse(
            description="Erro ao consultar a OpenLibrary."
        ),
        401: None,
        403: None,
    },
    tags=["Livros"],
)

    def get(self, request):
        
        try:
            q = request.query_params.get("q") 
            
            cache_key = f"livros_{q}"
            
            livros = cache.get(cache_key)
            
            if livros:
                return Response(livros)
            
            livros = busca_livro(q)
            
            cache.set(cache_key, livros, timeout=60)
        
            return Response(livros)
    
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=400
            )
        
    
    
class ImportarLivroView(APIView):
    
    permission_classes = [IsAuthenticated, isAdmin]
    
    @extend_schema(
    summary="Importar livro da OpenLibrary",
    description="""
    Importa um livro pesquisado na OpenLibrary para o banco de dados.

    Caso o livro já exista (mesmo `obra_id`), ele não será duplicado.
    """,
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "obra_id": {
                    "type": "string",
                    "example": "OL27448W"
                },
                "titulo": {
                    "type": "string",
                    "example": "Clean Code"
                },
                "autores": {
                    "type": "string",
                    "example": "Robert C. Martin"
                },
                "ano": {
                    "type": "integer",
                    "example": 2008
                },
                "editora": {
                    "type": "string",
                    "example": "Prentice Hall"
                }
            },
            "required": [
                "obra_id",
                "titulo",
                "autores"
            ]
        }
    },
    responses={
        201: OpenApiResponse(
            description="Livro importado com sucesso."
        ),
        200: OpenApiResponse(
            description="Livro já existia no banco."
        ),
        400: OpenApiResponse(
            description="Dados inválidos."
        ),
        401: None,
        403: None,
    },
    tags=["Livros"],
)
    
    def post(self, request):
        
        data = request.data
        
        livro, created = importar_livro(data)   
        
        serializer = LivroSerializer(livro)           
        
        return Response({
            "created": created,
            "livro": serializer.data
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

        livros = lista_livro(q, request.user)  
        
        paginator = DefaultPagination()
        
        page = paginator.paginate_queryset(
            livros, 
            request
        )
        
        serializer = LivroSerializer(page, many=True)
        
        return paginator.get_paginated_response(serializer.data)
       

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
        
            return Response(
                {"detail": f"{livro.titulo} removido."},
                status=200)
        
        
        except BookNotFoundError as e:
            return Response(
                {"detail": "Livro não encontrado."},
                status=404)
            
        except ActivateBookLoan as e:
            return Response(
                {"detail": "Livro com empréstimo ativo."}, 
                 status=409
            )
        
        

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
            
        except ValidationError as e:
            return Response(
                e.detail, 
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

        except BookNotFoundError:

            return Response({
                "detail": "Livro não encontrado."
            }, status=404)
            
        except ValidationError as e:
            return Response(
                e.detail, 
                status=400
            )
            
             
        
    




        
        