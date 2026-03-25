from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.views import View

from core.bases.views import (
    BaseServiceCreateView,
    BaseServiceListView,
    BaseServiceUpdateView,
)
from core.mixins import AppLoginRequiredMixin, FlashMessageMixin, ServiceObjectMixin
from finance.forms import CategoriaFilterForm, CategoriaForm, LancamentoFilterForm, LancamentoForm
from finance.services.categoria_service import CategoriaService
from finance.services.lancamento_service import LancamentoService


# ── Categorias ─────────────────────────────────────────────────────────────────

class CategoriaListView(BaseServiceListView):
    template_name = 'finance/categoria_list.html'
    partial_template_name = 'finance/partials/categoria_list_content.html'
    context_object_name = 'categorias'
    service_class = CategoriaService
    paginate_by = 15

    def get_filter_form(self):
        if not hasattr(self, '_filter_form'):
            self._filter_form = CategoriaFilterForm(data=self.request.GET or None)
        return self._filter_form

    def get_service_filters(self):
        form = self.get_filter_form()
        filters = {}
        if form.is_valid():
            nome = form.cleaned_data.get('nome')
            if nome:
                filters['nome__icontains'] = nome
        return filters

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.get_filter_form()
        context['page_title'] = 'Categorias'
        context['page_subtitle'] = 'Gerencie as categorias de receitas e despesas.'
        context['empty_title'] = 'Nenhuma categoria cadastrada'
        context['empty_description'] = 'Crie categorias para organizar seus lançamentos.'
        context['empty_action_url'] = reverse_lazy('finance:categoria_create')
        context['empty_action_label'] = 'Nova categoria'
        return context


class CategoriaCreateView(BaseServiceCreateView):
    template_name = 'finance/categoria_form.html'
    form_class = CategoriaForm
    service_class = CategoriaService
    success_url = reverse_lazy('finance:categoria_list')
    success_message = 'Categoria criada com sucesso.'

    def get_service_payload(self, form):
        return {k: v for k, v in form.cleaned_data.items()}


class CategoriaUpdateView(BaseServiceUpdateView):
    template_name = 'finance/categoria_form.html'
    form_class = CategoriaForm
    service_class = CategoriaService
    success_url = reverse_lazy('finance:categoria_list')
    success_message = 'Categoria atualizada com sucesso.'

    def get_service_payload(self, form):
        return {k: v for k, v in form.cleaned_data.items()}


class CategoriaDeleteView(AppLoginRequiredMixin, FlashMessageMixin, ServiceObjectMixin, View):
    service_class = CategoriaService
    success_message = 'Categoria removida com sucesso.'
    error_message = 'Não foi possível remover esta categoria.'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        return TemplateResponse(
            request,
            'finance/partials/categoria_delete_modal.html',
            {
                'categoria': instance,
                'delete_url': reverse('finance:categoria_delete', kwargs={'pk': instance.pk}),
            },
        )

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.get_service().delete(instance)
            self.add_success_message()
        except ValidationError as e:
            self.add_error_message(str(e.message))
        response = HttpResponse(status=204)
        response['HX-Trigger'] = 'categoriaChanged'
        return response


# ── Lançamentos ────────────────────────────────────────────────────────────────

class LancamentoListView(FlashMessageMixin, BaseServiceListView):
    template_name = 'finance/lancamento_list.html'
    partial_template_name = 'finance/partials/lancamento_list_content.html'
    context_object_name = 'lancamentos'
    service_class = LancamentoService
    paginate_by = 20

    def get_filter_form(self):
        if not hasattr(self, '_filter_form'):
            self._filter_form = LancamentoFilterForm(
                data=self.request.GET or None,
                user=self.request.user,
            )
        return self._filter_form

    def get_service_filters(self):
        form = self.get_filter_form()
        filters = {}
        if form.is_valid():
            if form.cleaned_data.get('tipo'):
                filters['tipo'] = form.cleaned_data['tipo']
            if form.cleaned_data.get('categoria'):
                filters['categoria'] = form.cleaned_data['categoria']
            if form.cleaned_data.get('data_inicio'):
                filters['data_inicio'] = form.cleaned_data['data_inicio']
            if form.cleaned_data.get('data_fim'):
                filters['data_fim'] = form.cleaned_data['data_fim']
        return filters

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.get_filter_form()
        context['page_title'] = 'Lançamentos'
        context['page_subtitle'] = 'Gerencie suas receitas e despesas.'
        context['empty_title'] = 'Nenhum lançamento encontrado'
        context['empty_description'] = 'Registre suas receitas e despesas para controlar seu saldo.'
        context['empty_action_url'] = ''
        context['empty_action_label'] = ''
        return context


class LancamentoModalCreateView(AppLoginRequiredMixin, View):
    def _get_tipo(self):
        return self.kwargs.get('tipo', 'RECEITA')

    def _build_context(self, form, tipo):
        url_name = f'finance:lancamento_create_{tipo.lower()}'
        return {
            'form': form,
            'tipo': tipo,
            'tipo_label': 'Receita' if tipo == 'RECEITA' else 'Despesa',
            'form_action': reverse(url_name),
        }

    def get(self, request, *args, **kwargs):
        tipo = self._get_tipo()
        form = LancamentoForm(user=request.user, tipo=tipo)
        return TemplateResponse(
            request,
            'finance/partials/lancamento_modal_form.html',
            self._build_context(form, tipo),
        )

    def post(self, request, *args, **kwargs):
        tipo = self._get_tipo()
        form = LancamentoForm(request.POST, user=request.user, tipo=tipo)
        if form.is_valid():
            LancamentoService(request).create(**form.cleaned_data)
            response = HttpResponse(status=204)
            response['HX-Trigger'] = 'lancamentoChanged'
            return response
        return TemplateResponse(
            request,
            'finance/partials/lancamento_modal_form.html',
            self._build_context(form, tipo),
        )


class LancamentoModalUpdateView(AppLoginRequiredMixin, ServiceObjectMixin, View):
    service_class = LancamentoService

    def _build_context(self, form, tipo, pk):
        return {
            'form': form,
            'tipo': tipo,
            'tipo_label': 'Receita' if tipo == 'RECEITA' else 'Despesa',
            'form_action': reverse('finance:lancamento_update', kwargs={'pk': pk}),
        }

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        tipo = instance.tipo
        form = LancamentoForm(instance=instance, user=request.user, tipo=tipo)
        return TemplateResponse(
            request,
            'finance/partials/lancamento_modal_form.html',
            self._build_context(form, tipo, instance.pk),
        )

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        tipo = instance.tipo
        form = LancamentoForm(request.POST, instance=instance, user=request.user, tipo=tipo)
        if form.is_valid():
            self.get_service().update(instance, **form.cleaned_data)
            response = HttpResponse(status=204)
            response['HX-Trigger'] = 'lancamentoChanged'
            return response
        return TemplateResponse(
            request,
            'finance/partials/lancamento_modal_form.html',
            self._build_context(form, tipo, instance.pk),
        )


class LancamentoDeleteView(AppLoginRequiredMixin, FlashMessageMixin, ServiceObjectMixin, View):
    service_class = LancamentoService
    success_message = 'Lançamento removido com sucesso.'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        return TemplateResponse(
            request,
            'finance/partials/lancamento_delete_modal.html',
            {
                'lancamento': instance,
                'delete_url': reverse('finance:lancamento_delete', kwargs={'pk': instance.pk}),
            },
        )

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        self.get_service().delete(instance)
        self.add_success_message()
        response = HttpResponse(status=204)
        response['HX-Trigger'] = 'lancamentoChanged'
        return response
