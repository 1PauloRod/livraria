from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('UserApp.urls')),
    path('livro/', include('LivroApp.urls')),
    path('emprestimo/', include('EmprestimoApp.urls')),

    # Schema OpenAPI
    path(
        'api/schema/',
        SpectacularAPIView.as_view(),
        name='schema'
    ),

    # Swagger UI
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),

    # ReDoc
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),
]