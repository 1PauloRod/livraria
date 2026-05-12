from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('UserApp.urls')), 
    path('livro/', include('LivroApp.urls')), 
    path('emprestimo/', include('EmprestimoApp.urls'))
]
