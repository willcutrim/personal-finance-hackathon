from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy


class AppLoginRequiredMixin(LoginRequiredMixin):
    """
    Mixin de autenticação com login_url padronizado para o projeto.

    Quando usar: em qualquer view que exija usuário autenticado.
    Substitui LoginRequiredMixin diretamente — só muda o login_url padrão.

    Exemplo:
        class MinhaView(AppLoginRequiredMixin, TemplateView):
            template_name = "minha_template.html"
    """

    login_url = reverse_lazy("accounts:login")


class HtmxRequestMixin:
    """
    Mixin para centralizar leitura de requisições HTMX na view.

    Quando usar: em views que precisam variar template/comportamento
    entre request completo e request parcial via HTMX.

    Requerimento recomendado:
        - `django_htmx.middleware.HtmxMiddleware` ativo.

    Fallback:
        - se o middleware não estiver ativo, usa o header HX-Request.
    """

    htmx_header_name = "HX-Request"

    def is_htmx_request(self):
        """Retorna True quando a requisição atual foi enviada via HTMX."""
        htmx_details = getattr(self.request, "htmx", None)
        if htmx_details is not None:
            return bool(htmx_details)
        return self.request.headers.get(self.htmx_header_name, "").lower() == "true"

    def get_htmx_redirect_response(self, url):
        """
        Retorna resposta de redirecionamento no padrão HTMX (HX-Redirect).

        Use quando a ação foi disparada via HTMX e o cliente precisa navegar
        para outra URL após sucesso.
        """
        response = HttpResponse(status=204)
        response["HX-Redirect"] = str(url)
        return response

    def redirect_response(self, url):
        """
        Retorna o redirecionamento correto para o tipo de request atual.

        - request normal: HttpResponseRedirect (302)
        - request HTMX: 204 com header HX-Redirect
        """
        if self.is_htmx_request():
            return self.get_htmx_redirect_response(url)
        return HttpResponseRedirect(str(url))


class AnonymousOnlyMixin:
    """
    Mixin que redireciona usuários já autenticados para outra página.

    Quando usar: em views públicas como login e cadastro, onde não faz
    sentido um usuário logado acessar.

    O que a view pode definir:
        - `redirect_url` (opcional): URL de destino para o usuário autenticado.
          Padrão: dashboard:painel.

    Exemplo:
        class LoginView(AnonymousOnlyMixin, FormView):
            ...
    """

    redirect_url = reverse_lazy("dashboard:painel")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)


class FlashMessageMixin:
    """
    Mixin para enviar mensagens flash de sucesso e erro via Django messages.

    Quando usar: em qualquer view que precise exibir feedback ao usuário
    após uma ação (criar, editar, deletar, login, etc.).

    O que a view pode definir:
        - `success_message` (str): mensagem exibida ao chamar add_success_message().
        - `error_message` (str): mensagem exibida ao chamar add_error_message().

    Métodos disponíveis:
        - `add_success_message(message=None)`: usa success_message ou mensagem avulsa.
        - `add_error_message(message=None)`: usa error_message ou mensagem avulsa.

    Exemplo:
        class CriarView(FlashMessageMixin, FormView):
            success_message = "Registro criado com sucesso."

            def form_valid(self, form):
                ...
                self.add_success_message()
                return redirect(self.success_url)
    """

    success_message = ""
    error_message = ""

    def add_success_message(self, message=None):
        """Envia mensagem de sucesso. Usa success_message da view se nenhuma for passada."""
        message = message or self.success_message
        if message:
            messages.success(self.request, message)

    def add_error_message(self, message=None):
        """Envia mensagem de erro. Usa error_message da view se nenhuma for passada."""
        message = message or self.error_message
        if message:
            messages.error(self.request, message)


class ServiceMixin:
    """
    Mixin que instancia e cacheia o service da view automaticamente.

    Quando usar: em qualquer view que precise acessar um service de domínio.
    Normalmente não é usado diretamente — as BaseViews já o incluem.

    O que a view DEVE definir:
        - `service_class`: a classe do service (subclasse de BaseService).

    Como funciona:
        - `get_service()` instancia `service_class(self.request)` na primeira
          chamada e armazena em `self._service` para reutilização.
        - O service recebe o request e internamente acessa self.user,
          eliminando a necessidade de passar user= em cada chamada.

    Exemplo:
        class CategoriaListView(ServiceMixin, ListView):
            service_class = CategoriaService

            def get_queryset(self):
                return self.get_service().list()  # user já está no service
    """

    service_class = None

    def get_service_class(self):
        """Retorna a classe do service. Sobrescreva para lógica dinâmica."""
        if self.service_class is None:
            raise ValueError(
                f"{self.__class__.__name__} deve definir `service_class` "
                "ou sobrescrever `get_service_class()`."
            )
        return self.service_class

    def get_service(self):
        """
        Retorna a instância cacheada do service para o request atual.
        Instancia na primeira chamada passando self.request ao __init__.
        """
        if not hasattr(self, "_service"):
            self._service = self.get_service_class()(self.request)
        return self._service


class ServiceObjectMixin(ServiceMixin):
    """
    Mixin que adiciona `get_object()` ao ServiceMixin, buscando o objeto
    pelo id na URL e validando via service (respeitando escopo do usuário).

    Quando usar: em views de detalhe, edição e exclusão que precisam
    buscar um objeto específico do usuário autenticado.

    O que a view pode definir:
        - `object_lookup_kwarg` (str): nome do parâmetro de URL com o id.
          Padrão: "pk".

    Comportamento:
        - Busca o objeto via `service.get_by_id(pk)`.
        - Lança Http404 se não encontrado (protege contra acesso cross-user).

    Exemplo:
        class CategoriaUpdateView(ServiceObjectMixin, BaseServiceFormView):
            service_class = CategoriaService
            object_lookup_kwarg = "pk"
    """

    object_lookup_kwarg = "pk"

    def get_object(self):
        """Busca o objeto pelo id da URL. Levanta Http404 se não encontrado."""
        object_id = self.kwargs.get(self.object_lookup_kwarg)
        instance = self.get_service().get_by_id(object_id)
        if not instance:
            raise Http404("Objeto não encontrado.")
        return instance
