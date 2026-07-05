from django.urls import path
from .views import ListaLivrosView, AdicionarLivroView, AtualizarLivroView, DeletarLivro, BuscaLivroOpenLibraryView, ImportarLivroView

urlpatterns = [
    path("buscar_livro/", BuscaLivroOpenLibraryView.as_view()), 
    path("importar/", ImportarLivroView.as_view()),
    path("listar/", ListaLivrosView.as_view()),
    path("adicionar/", AdicionarLivroView.as_view()), 
    path("atualizar/<int:livro_id>/", AtualizarLivroView.as_view()), 
    path("deletar/<int:livro_id>/", DeletarLivro.as_view())
]
