from django.contrib import admin
from .models import Livro, Autor, Editora, Mensagem, Estoque, Aluguel, Devolucao, Pedido, Genero
# Register your models here.


class LivroAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Livro, LivroAdmin)
admin.site.register(Autor)
admin.site.register(Editora)
admin.site.register(Mensagem)
admin.site.register(Estoque)
admin.site.register(Aluguel)
admin.site.register(Devolucao)
admin.site.register(Pedido)
admin.site.register(Genero)

