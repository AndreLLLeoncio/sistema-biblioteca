from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CriarUsuarioForm, PedidoForm
from .models import Livro

# Create your views here.

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
                return redirect('home')
            else:
                messages.info(request, "Nome de Usuario OU Senha incorretos")

        return render(request, 'accounts/login.html')




def sairUsuario(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    return render(request, 'accounts/dashboard.html')

@login_required(login_url='login')
def perfil(request):
    user = request.user
    return render(request, 'accounts/perfil.html', {'user': user})

@login_required(login_url='login')
def livrosPage(request):
    livros = Livro.objects.all()
    return render(request, 'accounts/livros/livros.html', {'livros': livros})


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
def livro(request, livro_id):
    livro = Livro.objects.get(pk=livro_id)
    autores = livro.fk_autor.all()
    generos = livro.genero_fk.all()
    if livro is not None:
        return render(request, 'accounts/livros/livro.html', {'livro': livro, 'autores': autores, 'generos': generos})
    else:
        raise Http404("Livro NAO Existe")
