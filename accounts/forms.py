from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Pedido, Livro, Aluguel, Autor


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
    class Meta:
        model = Aluguel
        exclude = ['prazo_devolucao']
'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
'''
