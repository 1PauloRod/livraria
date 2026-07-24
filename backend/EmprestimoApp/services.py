from .models import Livro
from .serializer import LivroSerializer
from LivroApp.models import Livro
from .models import Emprestimo
from .serializer import EmprestimoSerializer
from UserApp.models import User
from  django.utils import timezone
from datetime import timedelta
from LivroApp.exceptions import BookUnavailableError, BookAlreadyReturnedError
from django.db.models import Q

def lista_emprestimo(q, user):
    if q:
        livros = Livro.objects.filter(
                titulo__icontains=q
            ) | Livro.objects.filter(
                autor__icontains=q
        )
            
        emprestimos = Emprestimo.objects.filter(
                user = user,
                Livro=livros
        )
    else:
        emprestimos = Emprestimo.objects.filter(user = user)
    
    return emprestimos


def lista_todos_emprestimos(q=""):
    
    emprestimos = (
        Emprestimo.objects
        .select_related("user", "livro")
        .order_by("-data_emprestimo")
    )
    
    if q:
        emprestimos = emprestimos.filter(
            Q(user__email__icontains=q) |
            Q(user__name__icontains=q) |
            Q(user__last_name__icontains=q) |
            Q(livro__titulo__icontains=q) |
            Q(livro__autor__icontains=q)
        )
    
    return emprestimos

def alugar_livro(livro_id, user):
    
    livro = Livro.objects.get(id=livro_id) 
    
    if livro.quantidade < 1:
        raise BookUnavailableError("Livro indisponível.")
    
    if Emprestimo.objects.filter(livro = livro, 
                                 user = user, 
                                 data_devolucao=None).exists():
        raise BookUnavailableError("Usuário já alugou este livro.") 
    
    emprestimo = Emprestimo.objects.create(
        livro=livro,
        user=user, 
        data_prevista_devolucao = timezone.now() + timedelta(days=7)
    )

    livro.quantidade-=1
    livro.save()
    
    return emprestimo


def devolver_livro(emprestimo_id):
    
    emprestimo = Emprestimo.objects.get(id=emprestimo_id)
    
    if not emprestimo:
        raise Emprestimo.DoesNotExist() 
    
    if emprestimo.data_devolucao:
        raise BookAlreadyReturnedError("Livro já devolvido.")
        
    emprestimo.data_devolucao = timezone.now()
    emprestimo.save()

    emprestimo.livro.quantidade += 1
    emprestimo.livro.save()
    
    return emprestimo