from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Pedido, Livro, Aluguel, Autor, Estoque


class CriarUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        exclude = ['user_fk']
        
        
class EditarUsuarioForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class AdicionarLivroAdm(ModelForm):
    class Meta:
        model = Livro
        fields = ['isbn', 'nome', 'data_lançamento', 'cover', 'fk_autor', 'fk_editora', 'tipo', 'genero_fk']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class AdicionarAutorAdm(ModelForm):
    class Meta:
        model = Autor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})



class RegistrarAluguel(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        estoques_disponiveis_ids = Estoque.objects.filter(reservado=False, alugado=False).values_list('id', flat=True)
        self.fields['estoque_fk'].queryset = Estoque.objects.filter(id__in=estoques_disponiveis_ids)
        self.fields['estoque_fk'].label_from_instance = lambda obj: f"{obj.livro_fk.nome if obj.livro_fk else 'Livro não encontrado'} - Edição {obj.edicao}"
    class Meta:
        model = Aluguel
        fields = ['estoque_fk', 'user_fk', 'dias_alugados']


