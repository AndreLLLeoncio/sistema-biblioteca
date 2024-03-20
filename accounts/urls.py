from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login' ),
    path('sair/', views.sairUsuario, name='sair' ),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/uidb64/token/',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),



    path('', views.home, name='home'),
    path('perfil/', views.perfil, name='perfil'),
    path('alugados/', views.meusLivros, name='alugados'),
    path('livros/', views.livrosPage, name='livros'),
    path('livros/<int:livro_id>', views.livro, name= 'livro'),
    path('pedido/', views.pedidoPage, name='pedido' ),
    path('reservar_livro/<int:livro_id>', views.reservarLivro, name='reservar_livro'),




    path('adm/', views.pagina_inicial_adm, name='adm_home' ),
    path('adm/perfil', views.perfil_adm, name='perfil_adm' ),

    
    # Funcionalidades de Livros
    path('adm/livros', views.livros_adm, name='livros_adm' ),
    path('adm/livros/<int:livro_id>', views.livro_adm, name='livro_adm' ),
    path('alugar_livro/<int:livro_id>', views.alugar_livro, name='alugar_livro' ),
    path('deletar_livro_adm/<int:livro_id>', views.deletar_livro_adm, name='deletar_livro_adm'),
    path('adicionar_edicao_adm/', views.adicionar_edicao_adm, name='adicionar_edicao_adm'),
    path('adm/livros/adicionar_livro_adm', views.adicionar_livro_adm, name='adicionar_livro_adm' ),
    path('editar_livro_adm/<livro_id>', views.editar_livro_adm, name='editar_livro_adm' ),



    # CRUD de Autores
    path('adm/autores', views.autores_adm, name='autores_adm' ),
    path('deletar_autor_adm/<int:autor_id>', views.deletar_autor_adm, name='deletar_autor_adm'),
    path('editar_autor_adm/<autor_id>/', views.editar_autor_adm, name='editar_autor_adm'),

    # CRUD de Generos
    path('adm/generos', views.generos_adm, name='generos_adm' ),
    path('deletar_genero_adm/<int:genero_id>', views.deletar_genero_adm, name='deletar_genero_adm'),
    path('editar_genero_adm/<genero_id>/', views.editar_genero_adm, name='editar_genero_adm'),

    # CRUD de Editoras
    path('adm/editoras', views.editoras_adm, name='editoras_adm' ),
    path('deletar_editora_adm/<int:editora_id>', views.deletar_editora_adm, name='deletar_editora_adm'),
    path('editar_editora_adm/<editora_id>/', views.editar_editora_adm, name='editar_editora_adm'),



    path('adm/alugueis', views.alugueis_adm, name='alugueis_adm' ),
    path('adm/devolucoes', views.devolucoes_adm, name='devolucoes_adm' ),
    path('adm/pedidos', views.pagina_pedidos_adm, name='pedidos_adm' ),
    path('adm/pedidos/<int:pedido_id>', views.pedido_adm, name= 'pedido_adm'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)