from django.db import models

class Livro(models.Model):
    titulo = models.CharField(max_length=150)
    autor = models.CharField(max_length=150) 
    ano = models.PositiveIntegerField() 
    disponivel = models.BooleanField(default=True)

    def str(self):
        return f"{self.autor} - {self.autor}"
    
