from django.db import models

class Livro(models.Model):
    titulo = models.CharField(max_length=150)
    autor = models.CharField(max_length=150) 
    ano = models.PositiveIntegerField() 
    editora = models.CharField(max_length=150, null=True, blank=True)
    isbn = models.CharField(max_length=13, null=True, blank=True)
    disponivel = models.BooleanField(default=True)

    quantidade = models.PositiveIntegerField(default=1)

    def str(self):
        return f"{self.autor} - {self.autor}"
    
