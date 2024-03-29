from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import UpdateView
from django.http import Http404, JsonResponse, HttpResponse
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CriarUsuarioForm, PedidoForm, EditarUsuarioForm, AdicionarLivroAdm, RegistrarAluguel, AdicionarAutorAdm, DevolucaoForm, AluguelForm, AdicionarGeneroAdm, AdicionarEditoraAdm
from .models import Livro, Pedido, Autor, Genero, Estoque, Aluguel, Devolucao, Editora
from datetime import datetime, timedelta
from django.db.models import Count


# Create your views here.




# ============================================   ADM   ===========================================

#  Pagina Inicial do ADM
@login_required(login_url='login')
@staff_member_required
def pagina_inicial_adm(request):
    dataset = Livro.objects.values('tipo').annotate(total=Count('tipo')).order_by('tipo')
    tipos = [data['tipo'] for data in dataset]
    totais = [data['total'] for data in dataset]

    autores_dataset = Autor.objects.annotate(total_books=Count('livro')).order_by('nome')
    autores = [autor.nome for autor in autores_dataset]
    livros_por_autor = [autor.total_books for autor in autores_dataset]

    context = {
        'tipos': tipos,
        'totais': totais,
        'autores': autores,
        'livros_por_autor': livros_por_autor,
    }

    return render(request, 'accounts/adm/pagina_inicial_adm.html', context)


@login_required(login_url='login')
@staff_member_required
def perfil_adm(request):
    user = request.user
    if request.method == 'POST':
        user_form = EditarUsuarioForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Usuario Atualizado com Sucesso')
            return redirect(to='perfil')
    else:
        user_form = EditarUsuarioForm(instance=request.user)

    return render(request, 'accounts/adm/perfil_adm.html', {'user_form': user_form})



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
    autores = Autor.objects.all()
    query = request.GET.get('q')
    if query:
        livros = livros.filter(nome__icontains=query)

    autor_id = request.GET.get('autor')
    if autor_id:
        livros = livros.filter(fk_autor__id=autor_id)
    
    return render(request,'accounts/adm/livros_crud/livros_adm.html', {'livros': livros , 'autores': autores})

@login_required(login_url='login')
@staff_member_required
def livro_adm(request, livro_id):
    copia_disponivel = Estoque.objects.filter(livro_fk = livro_id, reservado=False, alugado=False).exists()
    livro = Livro.objects.get(pk=livro_id)
    autores = livro.fk_autor.all()
    generos = livro.genero_fk.all()
    if livro is not None:
        return render(request, 'accounts/adm/livros_crud/livro_adm.html', {'livro': livro, 'autores': autores, 'generos': generos, 'copia_disponivel':copia_disponivel})
    else:
        raise Http404("Livro NAO Existe")


@login_required(login_url='login')
@staff_member_required
def alugar_livro(request, livro_id):
    estoque_disponivel = Estoque.objects.filter(livro_fk=livro_id, reservado=False, alugado=False).order_by('id').first()
    if estoque_disponivel:
        if request.method == 'POST':
            form = AluguelForm(request.POST)
            if form.is_valid():
                aluguel = form.save(commit=False)
                aluguel.estoque_fk = estoque_disponivel
                aluguel.data_alugada = datetime.now()
                dias_alugados = aluguel.dias_alugados
                prazo_devolucao = datetime.now() + timedelta(days=dias_alugados)
                aluguel.prazo_devolucao = prazo_devolucao
                aluguel.save()

                estoque_pk = aluguel.estoque_fk.id
                estoque = Estoque.objects.get(pk=estoque_pk)
                estoque.fk_user = aluguel.user_fk
                estoque.alugado = True
                estoque.save()
                return redirect('livro_adm', livro_id=livro_id)
        else:
            form = AluguelForm()
        return render(request, 'accounts/adm/aluguel_adm.html', {'form': form})
    else:
        return redirect('livro_adm',livro_id=livro_id)
    


@login_required(login_url='login')
@staff_member_required
def deletar_livro_adm(request, livro_id):
    livro = Livro.objects.get(pk=livro_id)
    livro.delete()
    messages.success(request, 'Livro Deletado com Sucesso ')
    return redirect('livros_adm')

@login_required(login_url='login')
@staff_member_required
def adicionar_livro_adm(request):
    if request.method == 'POST':
        form = AdicionarLivroAdm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro Adicionado com Sucesso ')
            return redirect('adicionar_livro_adm')
    else:
        form = AdicionarLivroAdm()

    return render(request, 'accounts/adm/livros_crud/adicionar_livro_adm.html', {'form':form})


def editar_livro_adm(request, livro_id):
    livro = Livro.objects.get(pk=livro_id)
    if request.method == 'POST':
        form = AdicionarLivroAdm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro Editado com Sucesso ')
            return redirect('editar_livro_adm', livro.pk)
    else:
        form = AdicionarLivroAdm(instance=livro)
    return render(request, 'accounts/adm/livros_crud/editar_livro_adm.html', {'form': form})


@login_required(login_url='login')
@staff_member_required
def adicionar_edicao_adm(request):
    if request.method == 'POST':
        livro_id = request.POST.get('livro_id')
        num_copias = int(request.POST.get('num_copias'))
        livro = Livro.objects.get(pk=livro_id)

        maior_edicao = Estoque.objects.filter(livro_fk = livro).order_by('-edicao').first()
        if maior_edicao:
            proxima_edicao = maior_edicao.edicao + 1
        else:
            proxima_edicao = 1

        for i in range(proxima_edicao, proxima_edicao + num_copias):
            estoque = Estoque(livro_fk = livro, edicao=i)
            estoque.save()
        return redirect('livro_adm', livro_id=livro_id)
    else:
        return redirect('livro_adm')
    









# ADM  AUTOR

@login_required(login_url='login')
@staff_member_required
def autores_adm(request):
    autores = Autor.objects.all()

    if request.method == 'POST':
        form = AdicionarAutorAdm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Autor Adicionado com Sucesso ')
            return redirect('autores_adm')
    else:
        form = AdicionarAutorAdm()
        
    return render(request,'accounts/adm/autores_crud/autores_adm.html', {"autores": autores, 'form':form})


@login_required(login_url='login')
@staff_member_required
def deletar_autor_adm(request, autor_id):
    autor = Autor.objects.get(pk=autor_id)
    autor.delete()
    messages.success(request, 'Autor Deletado com Sucesso ')
    return redirect('autores_adm')



def editar_autor_adm(request, autor_id):
    autor = Autor.objects.get(pk=autor_id)
    if request.method == 'POST':
        form = AdicionarAutorAdm(request.POST, instance=autor)
        form.save()
        messages.success(request, 'Livro Editado com Sucesso ')
        return redirect('editar_autor_adm', autor.pk)
    else:
        form = AdicionarAutorAdm(instance=autor)
    return render(request, 'accounts/adm/autores_crud/editar_autor_adm.html', {'form': form})











# ADM  ALUGUEL

@login_required(login_url='login')
@staff_member_required
def alugueis_adm(request):
    if request.method == 'POST':
        form = RegistrarAluguel(request.POST)
        if form.is_valid():
            aluguel = form.save(commit=False)

            estoque_pk = aluguel.estoque_fk.id
            estoque = Estoque.objects.get(pk=estoque_pk)
            if estoque.reservado == False and estoque.alugado == False:

                estoque.fk_user = aluguel.user_fk
                estoque.alugado = True
                estoque.save()

                dias_alugados = aluguel.dias_alugados
                prazo_devolucao = datetime.now() + timedelta(days=dias_alugados)
                aluguel.prazo_devolucao = prazo_devolucao
                aluguel.data_alugada = datetime.now()
                form.save()
                messages.success(request, 'Livro Alugado com Successo')
                return redirect('alugueis_adm')
            else:
                messages.error(request, 'Livro Indisponivel para Aluguel')
                
            return redirect('alugueis_adm')
                
    else:
        form = RegistrarAluguel()

    alugueis = Aluguel.objects.all()


    return render(request,'accounts/adm/alugueis_adm.html', {'form': form, 'alugueis':alugueis})












# ADM  DEVOLUÇÕES

@login_required(login_url='login')
@staff_member_required
def devolucoes_adm(request):
    if request.method == 'POST':
        form = DevolucaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('devolucoes_adm') 
    else:
        form = DevolucaoForm()

    devolucoes = Devolucao.objects.all()
    return render(request, 'accounts/adm/devolucoes_adm.html', {'form': form, 'devolucoes':devolucoes})















# ADM  GENEROS

@login_required(login_url='login')
@staff_member_required
def generos_adm(request):
    generos = Genero.objects.all()
    if request.method == 'POST':
        form = AdicionarGeneroAdm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Genero Adicionado com Sucesso ')
            return redirect('generos_adm')
    else:
        form = AdicionarGeneroAdm()
    return render(request,'accounts/adm/generos_crud/generos_adm.html', {"generos":generos, 'form':form})

@login_required(login_url='login')
@staff_member_required
def deletar_genero_adm(request, genero_id):
    genero = Genero.objects.get(pk=genero_id)
    genero.delete()
    messages.success(request, 'Genero Deletado com Sucesso ')
    return redirect('generos_adm')

def editar_genero_adm(request, genero_id):
    genero = Genero.objects.get(pk=genero_id)
    if request.method == 'POST':
        form = AdicionarGeneroAdm(request.POST, instance=genero)
        form.save()
        messages.success(request, 'Genero Editado com Sucesso ')
        return redirect('editar_genero_adm', genero.pk)
    else:
        form = AdicionarGeneroAdm(instance=genero)
    return render(request, 'accounts/adm/generos_crud/editar_genero_adm.html', {'form': form})












# ADM  EDITORAS

@login_required(login_url='login')
@staff_member_required
def editoras_adm(request):
    editoras = Editora.objects.all()
    if request.method == 'POST':
        form = AdicionarEditoraAdm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Editora Adicionada com Sucesso ')
            return redirect('editoras_adm')
    else:
        form = AdicionarEditoraAdm()
    return render(request,'accounts/adm/editoras_crud/editoras_adm.html', {"editoras":editoras, 'form':form})

@login_required(login_url='login')
@staff_member_required
def deletar_editora_adm(request, editora_id):
    editora = Editora.objects.get(pk=editora_id)
    editora.delete()
    messages.success(request, 'Editora Deletada com Sucesso ')
    return redirect('editoras_adm')

def editar_editora_adm(request, editora_id):
    editora = Editora.objects.get(pk=editora_id)
    if request.method == 'POST':
        form = AdicionarEditoraAdm(request.POST, instance=editora)
        form.save()
        messages.success(request, 'Editora Editada com Sucesso ')
        return redirect('editar_editora_adm', editora.pk)
    else:
        form = AdicionarEditoraAdm(instance=editora)
    return render(request, 'accounts/adm/editoras_crud/editar_editora_adm.html', {'form': form})







# ============================================   Login / Cadastro / Logout   ===========================================


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





# ============================================   USUARIO   ===========================================


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

    return render(request, 'accounts/user/perfil.html', {'user_form': user_form})


@login_required(login_url='login')
def livrosPage(request):
    livros = Livro.objects.all()
    return render(request, 'accounts/livros/livros.html', {'livros': livros})


@login_required(login_url='login')
def livro(request, livro_id):
    copia_disponivel = Estoque.objects.filter(livro_fk = livro_id, reservado=False, alugado=False).exists()
    livro = Livro.objects.get(pk=livro_id)
    autores = livro.fk_autor.all()
    generos = livro.genero_fk.all()
    if livro is not None:
        return render(request, 'accounts/livros/livro.html', {'livro': livro, 'autores': autores, 'generos': generos, 'copia_disponivel':copia_disponivel })
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
    usuario = request.user
    alugueis_alugados = Aluguel.objects.filter(user_fk = usuario,estoque_fk__alugado=True)

    return render(request,'accounts/user/meus_livros.html', {'alugueis_alugados': alugueis_alugados})


@login_required(login_url='login')
def reservarLivro(request, livro_id):
    if Estoque.objects.filter(livro_fk = livro_id).exists():
        estoque_disponivel = Estoque.objects.filter(livro_fk = livro_id, reservado=False, alugado=False).order_by('id').first()
        if estoque_disponivel:
            estoque_disponivel.fk_user = request.user
            estoque_disponivel.reservado = True
            estoque_disponivel.save()
            messages.success(request, 'Livro Reservado com Successo')
        else:
            messages.error(request, 'Livro Indisponivel para Reserva')
    else:
        messages.error(request, 'Ainda não temos cópias para este livro')
    return redirect('livro',livro_id=livro_id)





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