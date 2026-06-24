from .models import Livro
from .serializer import LivroSerializer
from LivroApp.models import Livro
from .models import Emprestimo
from .serializer import EmprestimoSerializer
from UserApp.models import User
from  django.utils import timezone

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


def lista_todos_emprestimos(q):
    if q:
        usuario = User.objects.filter(
            email__icontains = q
        )
        emprestimos = User.objects.filter(
                user = usuario
        )

    emprestimos = Emprestimo.objects.all()

    return emprestimos

def alugar_livro(livro_id, user):
    
    livro = Livro.objects.get(id=livro_id) 
    
    if not livro:
        raise Livro.DoesNotExist() 
    
    if not livro.disponivel:
        raise ValueError("Livro indisponível")
    
    emprestimo = Emprestimo.objects.create(
        livro=livro,
        user=user
    )

    livro.disponivel = False
    livro.save()
    
    return emprestimo


def devolver_livro(emprestimo_id):
    
    emprestimo = Emprestimo.objects.get(id=emprestimo_id)
    
    if not emprestimo:
        raise Emprestimo.DoesNotExist() 
    
    if emprestimo.data_devolucao:
        ValueError("Livro já devolvido.")
        
    emprestimo.data_devolucao = timezone.now()
    emprestimo.save()

    emprestimo.livro.disponivel = True
    emprestimo.livro.save()
    
    return emprestimo