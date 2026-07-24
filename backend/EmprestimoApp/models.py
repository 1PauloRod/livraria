from django.db import models
from LivroApp.models import Livro
from UserApp.models import User
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

class Emprestimo(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE) 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateTimeField(null=True, blank=True)
    data_prevista_devolucao = models.DateTimeField()
    
    @property
    def dias_atraso(self):
        referencia = self.data_devolucao or timezone.now()
        
        atraso = (referencia.date() - self.data_prevista_devolucao.date()).days
        
        return max(atraso, 0)
    
    @property
    def multa(self):
        return self.dias_atraso * Decimal("3.00")