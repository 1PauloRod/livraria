from LivroApp.models import Livro
from EmprestimoApp.models import Emprestimo
from django.utils import timezone
from .serializer import LivroSerializer
import requests

def busca_livro(q):
    
    url = "https://openlibrary.org/search.json"

    response = requests.get(url, params={"q": q}, timeout=10)
    response.raise_for_status()
    
    data = response.json()

    livros = []

    for item in data.get("docs", [])[:10]:

        livros.append({
            "titulo": item.get("title"),
            "autores": item.get("author_name", []), 
            "ano": item.get("first_publish_year"),
            "isbn": (item.get("isbn") or [None])[0],
            "editora": item.get("publisher", []),
            "obra_id": item.get("key"),
            "capa_id": item.get("cover_i"),
        })

    return livros
    
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

    try:
        livro = Livro.objects.get(id=livro_id)
    except Livro.DoesNotExist:
        raise Livro.DoesNotExist("Livro não encontrado.") 
    
    emprestimo_ativo = Emprestimo.objects.filter(
                                            livro=livro, 
                                            user=user
                                        )
    if emprestimo_ativo:
            emprestimo_ativo.data_devolucao = timezone.now()
            emprestimo_ativo.save()
        
    livro.delete()

    return livro

def atualiza_livro(data, livro_id):
    
    try:
        livro = Livro.objects.get(id=livro_id)
        
    except Livro.DoesNotExist:
            raise Livro.DoesNotExist("Livro não existe.")
        
    return livro
    
    