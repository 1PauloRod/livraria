from django.core.management.base import BaseCommand
from faker import Faker
import random

from UserApp.models import User
from LivroApp.models import Livro
from EmprestimoApp.models import Emprestimo

fake = Faker('pt_BR')


class Command(BaseCommand):

    help = "Popula banco"

    def handle(self, *args, **kwargs):

        # limpar
        Emprestimo.objects.all().delete()
        Livro.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write(self.style.WARNING("Banco limpo"))

        # usuarios
        users = []

        for _ in range(20):

            user = User.objects.create_user(
                email=fake.unique.email(),
                password="123456",
                name=fake.first_name(),
                last_name=fake.last_name()
            )

            users.append(user)

        self.stdout.write(self.style.SUCCESS("Usuários criados"))

        # livros
        books = []

        for _ in range(100):

            book = Livro.objects.create(
                titulo=fake.sentence(nb_words=3),
                autor=fake.name(),
                ano=random.randint(1950, 2025),
                disponivel=True
            )

            books.append(book)

        self.stdout.write(self.style.SUCCESS("Livros criados"))

        # emprestimos
        for _ in range(30):

            book = random.choice(books)

            Emprestimo.objects.create(
                user=random.choice(users),
                livro=book
            )

            book.disponivel = False
            book.save()

        self.stdout.write(self.style.SUCCESS("Empréstimos criados"))