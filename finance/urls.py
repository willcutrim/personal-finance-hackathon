from django.urls import path

from finance.views import (
    CategoriaCreateView,
    CategoriaDeleteView,
    CategoriaListView,
    CategoriaUpdateView,
    LancamentoDeleteView,
    LancamentoListView,
    LancamentoModalCreateView,
    LancamentoModalUpdateView,
)

app_name = 'finance'

urlpatterns = [
    # Categorias
    path('categorias/', CategoriaListView.as_view(), name='categoria_list'),
    path('categorias/nova/', CategoriaCreateView.as_view(), name='categoria_create'),
    path('categorias/<int:pk>/editar/', CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categorias/<int:pk>/excluir/', CategoriaDeleteView.as_view(), name='categoria_delete'),

    # Lançamentos
    path('lancamentos/', LancamentoListView.as_view(), name='lancamento_list'),
    path('lancamentos/novo/receita/', LancamentoModalCreateView.as_view(), {'tipo': 'RECEITA'}, name='lancamento_create_receita'),
    path('lancamentos/novo/despesa/', LancamentoModalCreateView.as_view(), {'tipo': 'DESPESA'}, name='lancamento_create_despesa'),
    path('lancamentos/<int:pk>/editar/', LancamentoModalUpdateView.as_view(), name='lancamento_update'),
    path('lancamentos/<int:pk>/excluir/', LancamentoDeleteView.as_view(), name='lancamento_delete'),
]
