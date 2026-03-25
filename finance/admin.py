from django.contrib import admin

from finance.models import Categoria, Lancamento


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'user', 'criado_em')
    list_filter = ('tipo',)
    search_fields = ('nome', 'user__username')
    raw_id_fields = ('user',)


@admin.register(Lancamento)
class LancamentoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'tipo', 'data', 'categoria', 'user', 'criado_em')
    list_filter = ('tipo', 'categoria')
    search_fields = ('descricao', 'user__username')
    raw_id_fields = ('user', 'categoria')
    date_hierarchy = 'data'
