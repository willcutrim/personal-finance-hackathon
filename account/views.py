from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from account.forms import LoginForm, RegisterForm
from account.services.auth_service import AuthService
from core.bases.views import BaseTemplateView
from core.mixins import AnonymousOnlyMixin, AppLoginRequiredMixin, FlashMessageMixin, HtmxRequestMixin


class RegisterView(AnonymousOnlyMixin, FlashMessageMixin, HtmxRequestMixin, FormView):
    template_name = 'account/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('dashboard:painel')
    success_message = 'Seja bem-vindo! Sua conta foi criada com sucesso.'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = None
        return kwargs

    def form_valid(self, form):
        service = AuthService(self.request)
        try:
            user = service.register(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
            )
            self.add_success_message()
            service.login_user(user) 
            return self.redirect_response(self.get_success_url())
        except ValidationError as exc:
            message = exc.messages[0] if exc.messages else str(exc)
            if 'e-mail' in message.lower():
                form.add_error('email', message)
            elif 'usuário' in message.lower():
                form.add_error('username', message)
            else:
                form.add_error(None, message)
            return self.form_invalid(form)


class LoginView(AnonymousOnlyMixin, FlashMessageMixin, HtmxRequestMixin, FormView):
    template_name = 'account/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('dashboard:painel')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = None
        return kwargs

    def form_valid(self, form):
        service = AuthService(self.request)
        try:
            user = service.authenticate_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            service.login_user(user)
            return self.redirect_response(self.get_success_url())
        except ValidationError as exc:
            message = exc.messages[0] if exc.messages else str(exc)
            form.add_error(None, message)
            return self.form_invalid(form)


class LogoutView(AppLoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        from django.contrib.auth import logout
        logout(request)
        from django.http import HttpResponseRedirect
        from django.urls import reverse
        return HttpResponseRedirect(reverse('accounts:login'))


class ProfileView(BaseTemplateView):
    template_name = 'account/profile.html'


class SettingsView(BaseTemplateView):
    template_name = 'account/settings.html'
