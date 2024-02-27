from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Pedido
from django import forms

class CriarUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        exclude = ['user_fk']
        
        
        
        
class EditarUsuarioForm(forms.ModelForm):
    username = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    

    class Meta:
        model = User
        fields = ['username', 'email']
    
