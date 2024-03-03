from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.

class Autor(models.Model):
    nome= models.CharField(max_length=50)
    data_nascimento = models.DateField()
    nacionalidade = models.CharField( max_length=50)
    
    def __str__(self):
        return self.nome


class Editora(models.Model):
    nome = models.CharField(max_length=50)
    data_inalguração = models.DateField()
    nacionalidade = models.CharField( max_length=50)
    endereço = models.CharField(max_length=50)
    telefone = models.DecimalField(max_digits=12,  decimal_places=0)

    def __str__(self):
        return self.nome


class Genero(models.Model):
    nome = models.CharField(max_length=50)
    area = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Livro(models.Model):
    isbn = models.DecimalField(max_digits=13, decimal_places=0)
    nome = models.CharField(max_length=50)
    data_lançamento = models.DateField()
    cover = models.ImageField(null=True, blank=True, upload_to='images/', max_length=255 )
    fk_autor = models.ManyToManyField(Autor)
    fk_editora = models.ForeignKey(Editora,null=True, blank=True, on_delete= models.SET_NULL)
    tipo = models.CharField(null=True, blank=True, max_length=50)
    genero_fk = models.ManyToManyField(Genero)


class Estoque(models.Model):
    livro_fk = models.ForeignKey(Livro,null=True, blank=True, on_delete= models.SET_NULL)
    edicao = models.IntegerField()



class Aluguel(models.Model):
    estoque_fk = models.ForeignKey(Estoque, null=True, blank=True, on_delete= models.SET_NULL)
    user_fk = models.ForeignKey(User, null=True, blank=True, on_delete= models.SET_NULL)
    data_alugada = models.DateField(auto_now_add= True)
    dias_alugados = models.IntegerField()
    prazo_devolucao = models.DateField()


class Devolucao(models.Model):
    estoque_fk = models.ForeignKey(Estoque, null=True, blank=True, on_delete= models.SET_NULL)
    user_fk = models.ForeignKey(User, null=True, blank=True, on_delete= models.SET_NULL)
    data_devolucao = models.DateField(auto_now_add= True)


class Mensagem(models.Model):
    user_fk = models.ForeignKey(User,null=True, blank=True, on_delete= models.SET_NULL)
    descricao = models.TextField()
    arquivo = models.FileField(null=True, blank=True, upload_to='docs/')


class Pedido(models.Model):
    user_fk = models.ForeignKey(User,null=True, blank=True, on_delete= models.SET_NULL)
    nome_livro = models.CharField(max_length=50)
    autor = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    genero = models.CharField(max_length=200)
    descricao_pedido = models.TextField()