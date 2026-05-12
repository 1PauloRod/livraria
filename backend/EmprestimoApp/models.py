from django.db import models
from LivroApp.models import Livro
from UserApp.models import User

class Emprestimo(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE) 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateTimeField(null=True, blank=True)
    

