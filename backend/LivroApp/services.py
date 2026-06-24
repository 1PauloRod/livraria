from LivroApp.models import Livro
from EmprestimoApp.models import Emprestimo
from django.utils import timezone
from .serializer import LivroSerializer

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
    
    