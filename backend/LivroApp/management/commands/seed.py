from django.core.management.base import BaseCommand
from faker import Faker
import random
from LivroApp.models import Livro
from EmprestimoApp.models import Emprestimo
from django.contrib.auth import get_user_model

fake = Faker("pt_BR") 
User = get_user_model()


'''
livros = [
    {"titulo": "Programming TypeScript", "autor": "Boris Cherny", "ano": 2019, "editora": "O'Reilly", "obra_id": "BK00261", "quantidade": 3},
    {"titulo": "Learning Java", "autor": "Marc Loy", "ano": 2020, "editora": "O'Reilly", "obra_id": "BK00262", "quantidade": 4},
    {"titulo": "Java Performance", "autor": "Scott Oaks", "ano": 2020, "editora": "O'Reilly", "obra_id": "BK00263", "quantidade": 2},
    {"titulo": "Modern Java in Action", "autor": "Raoul-Gabriel Urma", "ano": 2019, "editora": "Manning", "obra_id": "BK00264", "quantidade": 5},
    {"titulo": "Reactive Design Patterns", "autor": "Roland Kuhn", "ano": 2017, "editora": "Manning", "obra_id": "BK00265", "quantidade": 3},
    {"titulo": "Reactive Messaging Patterns with the Actor Model", "autor": "Vaughn Vernon", "ano": 2015, "editora": "Addison-Wesley", "obra_id": "BK00266", "quantidade": 2},
    {"titulo": "Akka in Action", "autor": "Raymond Roestenburg", "ano": 2016, "editora": "Manning", "obra_id": "BK00267", "quantidade": 3},
    {"titulo": "Reactive Spring", "autor": "Josh Long", "ano": 2020, "editora": "Addison-Wesley", "obra_id": "BK00268", "quantidade": 4},
    {"titulo": "Spring Boot in Action", "autor": "Craig Walls", "ano": 2016, "editora": "Manning", "obra_id": "BK00269", "quantidade": 3},
    {"titulo": "Spring Microservices in Action", "autor": "John Carnell", "ano": 2021, "editora": "Manning", "obra_id": "BK00270", "quantidade": 2},
]'''

class Command(BaseCommand):

    help = "Popula o banco com livros"

    def handle(self, *args, **kwargs):

        '''for livro in livros:
            Livro.objects.get_or_create(
                obra_id = livro["obra_id"], 
                defaults={
                    **livro
                }
            )'''
            
        
        for i in range(50):
            user = User.objects.order_by("?").first()
            livro = Livro.objects.order_by("?").first()
            Emprestimo.objects.get_or_create(
                user=user, 
                livro=livro
            )
            
        self.stdout.write(
            self.style.SUCCESS("Empréstimos criados com sucesso!")
        )
            