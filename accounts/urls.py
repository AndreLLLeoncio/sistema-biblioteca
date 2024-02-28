from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.home, name='home'),
    path('perfil/', views.perfil, name='perfil'),
    path('livros/', views.livrosPage, name='livros'),
    path('livros/<int:livro_id>', views.livro, name= 'livro'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login' ),
    path('sair/', views.sairUsuario, name='sair' ),
    path('pedido/', views.pedidoPage, name='pedido' ),
    path('atualizar_usuario/', views.aualizarUsuario, name='atualizar_usuario'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)