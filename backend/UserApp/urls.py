from django.urls import path
from .views import RegisterView, LoginView, LogoutView, MeView, ListaUsuarios, DeletaUsuario

urlpatterns = [
    path("register/", RegisterView.as_view()), 
    path("login/", LoginView.as_view()), 
    path("logout/", LogoutView.as_view()), 
    path("me/", MeView.as_view()), 
    path("listar/", ListaUsuarios.as_view()), 
    path("deletar/<int:user_id>/", DeletaUsuario.as_view())
]
