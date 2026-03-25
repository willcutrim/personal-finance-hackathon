from django.core.exceptions import ValidationError
from django.utils.cache import patch_vary_headers
from django.views.generic import FormView, ListView, TemplateView

from core.mixins import (
    AppLoginRequiredMixin,
    FlashMessageMixin,
    HtmxRequestMixin,
    ServiceMixin,
    ServiceObjectMixin,
)


class BaseTemplateView(AppLoginRequiredMixin, TemplateView):
    """
    View base para páginas simples que não precisam de service.

    Quando usar: dashboards, perfil, configurações — páginas que só
    renderizam um template com dados do contexto.

    Já inclui: autenticação obrigatória (AppLoginRequiredMixin).

    Exemplo:
        class PerfilView(BaseTemplateView):
            template_name = "account/profile.html"
    """

    pass


class BaseServiceListView(AppLoginRequiredMixin, HtmxRequestMixin, ServiceMixin, ListView):
    """
    View base para listagem de registros via service.

    Quando usar: páginas de listagem que filtram por usuário autenticado.

    O que a view DEVE definir:
        - `service_class`: service de domínio (subclasse de BaseService).
        - `template_name`: template de listagem.
        - `partial_template_name`: fragmento usado para requests HTMX.

    O que a view PODE sobrescrever:
        - `get_service_filters()`: retorna dict de filtros extras para o service.
        - `context_object_name`: nome da variável no template (padrão: "objetos").
        - `paginate_by`: paginação (padrão: 10).

    Exemplo:
        class CategoriaListView(BaseServiceListView):
            template_name = "finance/categoria_list.html"
            partial_template_name = "finance/partials/categoria_list_content.html"
            context_object_name = "categorias"
            service_class = CategoriaService
    """

    context_object_name = "objetos"
    partial_template_name = None
    paginate_by = 10
    list_container_id = "list-content"
    list_hx_swap = "outerHTML"
    list_hx_push_url = "true"
    list_hx_enabled = True

    def get_partial_template_name(self):
        """
        Template parcial usado nas requisições HTMX.
        Se não definido, reutiliza o template principal.
        """
        return self.partial_template_name or self.template_name

    def get_service_filters(self):
        """Retorna filtros adicionais a serem passados para service.list(). Sobrescreva se necessário."""
        return {}

    def get_template_names(self):
        if self.is_htmx_request():
            return [self.get_partial_template_name()]
        return super().get_template_names()

    def get_list_hx_target(self):
        """Retorna o seletor CSS do container da listagem que será trocado pelo HTMX."""
        return f"#{self.list_container_id}"

    def get_queryset(self):
        return self.get_service().list(**self.get_service_filters())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("list_container_id", self.list_container_id)
        context.setdefault("list_partial_template", self.get_partial_template_name())
        context.setdefault("list_hx_enabled", self.list_hx_enabled)
        context.setdefault("list_hx_target", self.get_list_hx_target())
        context.setdefault("list_hx_swap", self.list_hx_swap)
        context.setdefault("list_hx_push_url", self.list_hx_push_url)
        context.setdefault("list_filter_form_id", "list-filter-form")
        return context

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        patch_vary_headers(response, ("HX-Request",))
        return response


class BaseServiceFormView(AppLoginRequiredMixin, HtmxRequestMixin, ServiceMixin, FlashMessageMixin, FormView):
    """
    View base para formulários de criação/edição via service.

    Usada internamente por BaseServiceCreateView e BaseServiceUpdateView.
    Normalmente não é usada diretamente.

    Já inclui: autenticação, acesso ao service e flash messages.

    O que a view DEVE definir:
        - `service_class`: service de domínio.
        - `form_class`: formulário Django.
        - `success_url` ou sobrescrever `get_success_url()`.

    Injeta `user` no formulário automaticamente via get_form_kwargs().
    """

    success_url = None

    def get_success_url(self):
        if not self.success_url:
            raise ValueError(
                f"{self.__class__.__name__} deve definir `success_url` "
                "ou sobrescrever `get_success_url()`."
            )
        return str(self.success_url)

    def get_form_kwargs(self):
        """Injeta o usuário autenticado no formulário (espera-se que o form aceite user=)."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class BaseServiceCreateView(BaseServiceFormView):
    """
    View base para criação de registros via service.

    Quando usar: formulário de criação de qualquer entidade.

    O que a view DEVE definir:
        - `service_class`, `form_class`, `template_name`, `success_url`.

    O que a view PODE sobrescrever:
        - `get_service_payload(form)`: extrai os dados do form antes de criar.
          Padrão: retorna form.cleaned_data inteiro.
        - `success_message`: mensagem exibida após criação bem-sucedida.

    Exemplo:
        class CategoriaCreateView(BaseServiceCreateView):
            template_name = "finance/categoria_form.html"
            form_class = CategoriaForm
            service_class = CategoriaService
            success_url = reverse_lazy("finance:categoria_list")
            success_message = "Categoria criada com sucesso."
    """

    def get_service_payload(self, form):
        """Extrai dados do form para passar ao service.create(). Sobrescreva para transformações."""
        return form.cleaned_data

    def form_valid(self, form):
        self.object = self.get_service().create(**self.get_service_payload(form))
        self.add_success_message()
        return self.redirect_response(self.get_success_url())


class BaseServiceUpdateView(ServiceObjectMixin, BaseServiceFormView):
    """
    View base para edição de registros via service.

    Quando usar: formulário de edição de uma entidade existente, identificada
    pelo `pk` na URL.

    O que a view DEVE definir:
        - `service_class`, `form_class`, `template_name`, `success_url`.

    O que a view PODE sobrescrever:
        - `get_service_payload(form)`: extrai os dados do form antes de atualizar.
        - `object_lookup_kwarg`: nome do parâmetro de URL (padrão: "pk").
        - `success_message`: mensagem exibida após edição bem-sucedida.

    Injeta a instância atual no formulário via get_form_kwargs() (instance=).

    Exemplo:
        class CategoriaUpdateView(BaseServiceUpdateView):
            template_name = "finance/categoria_form.html"
            form_class = CategoriaForm
            service_class = CategoriaService
            success_url = reverse_lazy("finance:categoria_list")
            success_message = "Categoria atualizada com sucesso."
    """

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.get_object()
        return kwargs

    def get_service_payload(self, form):
        """Extrai dados do form para passar ao service.update(). Sobrescreva para transformações."""
        return form.cleaned_data

    def form_valid(self, form):
        self.object = self.get_service().update(self.get_object(), **self.get_service_payload(form))
        self.add_success_message()
        return self.redirect_response(self.get_success_url())


class BaseServiceDeleteView(
    ServiceObjectMixin, AppLoginRequiredMixin, HtmxRequestMixin, FlashMessageMixin, TemplateView
):
    """
    View base para exclusão de registros via service.

    Quando usar: página de confirmação de exclusão + processamento via POST.

    O que a view DEVE definir:
        - `service_class`, `template_name`, `success_url`.

    O que a view PODE sobrescrever:
        - `context_object_name`: nome do objeto no template (padrão: "objeto").
        - `success_message`: mensagem após exclusão bem-sucedida.
        - `error_message`: mensagem padrão se ValidationError sem mensagem própria.
        - `object_lookup_kwarg`: parâmetro de URL (padrão: "pk").

    Tratamento automático de ValidationError:
        Se o service.delete() levantar ValidationError (ex: não pode excluir
        categoria com lançamentos), a mensagem de erro é exibida via flash
        e o usuário é redirecionado para success_url — sem necessidade de
        try/except na view.

    Exemplo:
        class CategoriaDeleteView(BaseServiceDeleteView):
            template_name = "finance/categoria_confirm_delete.html"
            service_class = CategoriaService
            success_url = reverse_lazy("finance:categoria_list")
            success_message = "Categoria removida com sucesso."
            context_object_name = "categoria"
    """

    success_url = None
    context_object_name = "objeto"

    def get_success_url(self):
        if not self.success_url:
            raise ValueError(
                f"{self.__class__.__name__} deve definir `success_url` "
                "ou sobrescrever `get_success_url()`."
            )
        return str(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = self.get_object()
        return context

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.get_service().delete(instance)
            self.add_success_message()
        except ValidationError as exc:
            error_msg = exc.messages[0] if exc.messages else str(exc)
            self.add_error_message(error_msg)
        return self.redirect_response(self.get_success_url())
