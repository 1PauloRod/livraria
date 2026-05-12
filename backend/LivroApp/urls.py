from django.urls import path
from .views import ListaLivrosView, AdicionarLivroView, AtualizarLivroView, DeletarLivro

urlpatterns = [
    path("listar/", ListaLivrosView.as_view()),
    path("adicionar/", AdicionarLivroView.as_view()), 
    path("atualizar/<int:livro_id>/", AtualizarLivroView.as_view()), 
    path("deletar/<int:livro_id>/", DeletarLivro.as_view())
]
