from django.urls import path
from .views import ListaEmprestimo, AlugarLivroView, DevolverLivro, ListaTodosEmprestimosView

urlpatterns = [
    path("listar/", ListaEmprestimo.as_view()),
    path("listar/todos/", ListaTodosEmprestimosView.as_view()), 
    path("alugar/<int:livro_id>/", AlugarLivroView.as_view()), 
    path("devolver/<int:emprestimo_id>/", DevolverLivro.as_view())
]
