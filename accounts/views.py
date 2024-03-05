from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from .forms import CriarUsuarioForm, PedidoForm, EditarUsuarioForm, AdicionarLivroAdm
from bootstrap_modal_forms.generic import BSModalCreateView
from .models import Livro, Pedido, Autor, Genero, Editora

# Create your views here.




#   ADM

#  Pagina Inicial do ADM
@login_required(login_url='login')
@staff_member_required
def pagina_inicial_adm(request):
    return render(request,'accounts/adm/pagina_inicial_adm.html')



# ADM  Pedido
@login_required(login_url='login')
@staff_member_required
def pagina_pedidos_adm(request):
    pedidos = Pedido.objects.all()
    return render(request,'accounts/adm/pedidos_adm.html', {'pedidos': pedidos})

@login_required(login_url='login')
@staff_member_required
def pedido_adm(request, pedido_id):
    pedido = Pedido.objects.get(pk=pedido_id)
    if pedido is not None:
        return render(request, 'accounts/adm/pedido_adm.html', {'pedido': pedido})
    else:
        raise Http404("Pedido NAO Existe")
    




# ADM  Livro

@login_required(login_url='login')
@staff_member_required
def livros_adm(request):
    livros = Livro.objects.prefetch_related('fk_autor')
    return render(request,'accounts/adm/livros_adm.html', {'livros': livros})

@login_required(login_url='login')
@staff_member_required
def livro_adm(request, livro_id):
    livro = Livro.objects.get(pk=livro_id)
    autores = livro.fk_autor.all()
    generos = livro.genero_fk.all()
    if livro is not None:
        return render(request, 'accounts/adm/livros_crud/livro_adm.html', {'livro': livro, 'autores': autores, 'generos': generos})
    else:
        raise Http404("Livro NAO Existe")

@login_required(login_url='login')
@staff_member_required
def deletar_livro_adm(request, livro_id):
    livro = Livro.objects.get(pk=livro_id)
    livro.delete()
    return redirect('livros_adm')

@login_required(login_url='login')
@staff_member_required
def adicionar_livro_adm(request):
    if request.method == 'POST':
        form = AdicionarLivroAdm(request.POST)
        if form.is_valid():
            livro = form.save(commit=False)
            livro.save()
            messages.success(request, 'Livro Adicionado com Sucesso ')
            return redirect('adicionar_livro_adm')
    else:
        form = AdicionarLivroAdm()
    
    autores = Autor.objects.all()
    generos = Genero.objects.all()
    editoras = Editora.objects.all()

    return render(request, 'accounts/adm/livros_crud/adicionar_livro_adm.html', {'form':form, 'autores': autores, 'generos':generos, 'editoras':editoras})



# ADM  AUTOR


@login_required(login_url='login')
@staff_member_required
def autores_adm(request):
    autores = Autor.objects.all()
    return render(request,'accounts/adm/autores_adm.html', {"autores": autores})


@login_required(login_url='login')
@staff_member_required
def generos_adm(request):
    return render(request,'accounts/adm/generos_adm.html')


@login_required(login_url='login')
@staff_member_required
def alugueis_adm(request):
    return render(request,'accounts/adm/alugueis_adm.html')


@login_required(login_url='login')
@staff_member_required
def devolucoes_adm(request):
    return render(request,'accounts/adm/devolucoes_adm.html')







# ADM  GENEROS

@login_required(login_url='login')
@staff_member_required
def generos_adm(request):
    generos = Genero.objects.all()
    return render(request,'accounts/adm/generos_adm.html', {"generos":generos})




# Login / Cadastro / Logout


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    else:
        form = CriarUsuarioForm()

        if request.method == 'POST':
            form = CriarUsuarioForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Conta criada para '+user)
                return redirect('login')

        context = {'form':form}
        return render(request, 'accounts/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    else:

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if user.is_staff == 1:
                    return redirect('adm_home')
                else:
                    return redirect('home')
            else:
                messages.info(request, "Nome de Usuario OU Senha incorretos")

        return render(request, 'accounts/login.html')


def sairUsuario(request):
    logout(request)
    return redirect('login')





# USUARIO


@login_required(login_url='login')
def home(request):
    return render(request, 'accounts/dashboard.html')


@login_required(login_url='login')
def perfil(request):
    user = request.user
    if request.method == 'POST':
        user_form = EditarUsuarioForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Usuario Atualizado com Sucesso')
            return redirect(to='perfil')
    else:
        user_form = EditarUsuarioForm(instance=request.user)

    return render(request, 'accounts/perfil.html', {'user_form': user_form})


@login_required(login_url='login')
def livrosPage(request):
    livros = Livro.objects.all()
    return render(request, 'accounts/livros/livros.html', {'livros': livros})


@login_required(login_url='login')
def livro(request, livro_id):
    livro = Livro.objects.get(pk=livro_id)
    autores = livro.fk_autor.all()
    generos = livro.genero_fk.all()
    if livro is not None:
        return render(request, 'accounts/livros/livro.html', {'livro': livro, 'autores': autores, 'generos': generos})
    else:
        raise Http404("Livro NAO Existe")
    

@login_required(login_url='login')
def pedidoPage(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.user_fk = request.user
            pedido.save()
            messages.success(request, 'Pedido Feito com Sucesso ')
            return redirect('pedido')
    else:
        form = PedidoForm()

    return render(request, 'accounts/pedido.html', {'form':form})


@login_required(login_url='login')
def meusLivros(request):
    return render(request, 'accounts/user/meus_livros.html')





def test(request):
    if request.method == 'POST':
        user_form = EditarUsuarioForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='test')
    else:
        user_form = EditarUsuarioForm(instance=request.user)
    return render(request, 'accounts/test1.html', {'user_form': user_form})