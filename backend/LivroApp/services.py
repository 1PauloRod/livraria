from LivroApp.models import Livro
from EmprestimoApp.models import Emprestimo
from django.utils import timezone
from .serializer import LivroSerializer
import requests
from .exceptions import BookNotFoundError

def busca_livro(q):
    
    url = "https://openlibrary.org/search.json"

    response = requests.get(url, params={"q": q}, timeout=10)
    response.raise_for_status()
    
    data = response.json()

    livros = []

    for item in data.get("docs", [])[:10]:

        livros.append({
            "titulo": item.get("title"),
            "autores": ", ".join(item.get("author_name", [])),
            "ano": item.get("first_publish_year"),
            "editora": ", ".join(item.get("publisher", [])),
            "obra_id": item.get("key"),
            "capa_id": item.get("cover_i"),
        })
        

    return livros

def importar_livro(data):
    livro, created = Livro.objects.get_or_create(
        obra_id=data["obra_id"],
        defaults={
        "titulo": data["titulo"],
        "autor": data["autores"],
        "ano": data["ano"],
        "editora": data["editora"],
            }
    )      
    
    return livro, created         
    
def lista_livro(q):
    if q:
        livros = Livro.objects.filter(
                titulo__icontains=q
        ) | Livro.objects.filter(
                autor__icontains=q
        )
    else:
        livros = Livro.objects.all()

    return livros

def deleta_livro(livro_id, user):

    livro = Livro.objects.filter(id=livro_id).first()

    if not livro:
        raise BookNotFoundError("Livro não encontrado.")

    emprestimo = Emprestimo.objects.filter(
        livro=livro,
        data_devolucao__isnull=True
    ).first()

    if emprestimo:
        emprestimo.data_devolucao = timezone.now()
        emprestimo.save()

    livro.delete()

    return livro

def atualiza_livro(data, livro_id):
    
    try:
        livro = Livro.objects.get(id=livro_id)
        
    except Livro.DoesNotExist:
            raise Livro.DoesNotExist("Livro não existe.")
        
    return livro
    
    