from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from account.forms import ChangePasswordForm, LoginForm, ProfileEditForm, RegisterForm
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


class ProfileEditModalView(AppLoginRequiredMixin, FlashMessageMixin, View):
    success_message = 'Perfil atualizado com sucesso.'

    def get(self, request, *args, **kwargs):
        form = ProfileEditForm(user=request.user)
        return TemplateResponse(
            request,
            'account/partials/profile_edit_modal.html',
            {'form': form},
        )

    def post(self, request, *args, **kwargs):
        form = ProfileEditForm(request.POST, user=request.user)
        if form.is_valid():
            service = AuthService(request)
            try:
                service.update_profile(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                )
                self.add_success_message()
                response = HttpResponse(status=204)
                response['HX-Trigger'] = 'profileChanged'
                return response
            except ValidationError as exc:
                message = exc.messages[0] if exc.messages else str(exc)
                form.add_error('email', message)
        return TemplateResponse(
            request,
            'account/partials/profile_edit_modal.html',
            {'form': form},
        )


class SettingsView(AppLoginRequiredMixin, FlashMessageMixin, HtmxRequestMixin, FormView):
    template_name = 'account/settings.html'
    form_class = ProfileEditForm
    success_url = reverse_lazy('accounts:settings')
    success_message = 'Perfil atualizado com sucesso.'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        service = AuthService(self.request)
        try:
            service.update_profile(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
            )
            self.add_success_message()
            return self.redirect_response(self.get_success_url())
        except ValidationError as exc:
            message = exc.messages[0] if exc.messages else str(exc)
            form.add_error('email', message)
            return self.form_invalid(form)


class ChangePasswordView(AppLoginRequiredMixin, FlashMessageMixin, HtmxRequestMixin, FormView):
    template_name = 'account/change_password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('accounts:change_password')
    success_message = 'Senha alterada com sucesso.'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        service = AuthService(self.request)
        service.change_password(new_password=form.cleaned_data['new_password1'])
        self.add_success_message()
        return self.redirect_response(self.get_success_url())
