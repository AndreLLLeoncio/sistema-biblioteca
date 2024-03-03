from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login' ),
    path('sair/', views.sairUsuario, name='sair' ),

    path('', views.home, name='home'),
    path('perfil/', views.perfil, name='perfil'),
    path('alugados/', views.meusLivros, name='alugados'),
    path('livros/', views.livrosPage, name='livros'),
    path('livros/<int:livro_id>', views.livro, name= 'livro'),
    path('pedido/', views.pedidoPage, name='pedido' ),


    path('test/', views.test, name='test' ),


    path('adm/', views.pagina_inicial_adm, name='adm_home' ),
    path('adm/pedidos', views.pagina_pedidos_adm, name='pedidos_adm' ),
    path('adm/livros', views.livros_adm, name='livros_adm' ),
    path('adm/livros/<int:livro_id>', views.livro_adm, name='livro_adm' ),
    path('deletar_livro_adm/<livro_id>', views.deletar_livro_adm, name='deletar_livro_adm'),
    path('adm/livros/adicionar_livro_adm', views.adicionar_livro_adm, name='adicionar_livro_adm' ),


    path('adm/autores', views.autores_adm, name='autores_adm' ),
    path('adm/generos', views.generos_adm, name='generos_adm' ),
    path('adm/alugueis', views.alugueis_adm, name='alugueis_adm' ),
    path('adm/devolucoes', views.devolucoes_adm, name='devolucoes_adm' ),
    path('adm/pedidos/<int:pedido_id>', views.pedido_adm, name= 'pedido_adm'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)