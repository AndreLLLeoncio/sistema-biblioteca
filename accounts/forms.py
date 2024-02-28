from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Pedido
from django import forms
from bootstrap_modal_forms.forms import  BSModalModelForm

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
    
