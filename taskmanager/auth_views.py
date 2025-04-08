
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import TemplateView

from .auth_forms import LoginForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate

# signup
class SignupView(TemplateView):
    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'form': UserCreationForm()})
    
    def post(self, request, *args, **kwargs):
       
        form = UserCreationForm(request.POST)

        if form.is_valid():
            # save user
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # log user in
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return HttpResponseRedirect(reverse('index'))

        return render(request, self.template_name, context={'form': form})

# login
class LoginView(TemplateView):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'form': LoginForm()})
    
    def post(self, request, *args, **kwargs):

        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # log user in
            user = authenticate(username=username, password=password)

            print(user)

            if user is not None:
                login(request, user)

                return HttpResponseRedirect(reverse('index'))

        return render(request, self.template_name, context={'form': form, 'login_status': 'invalid username or password'})        



# logout
class LogoutView(TemplateView):
    template_name = 'accounts/logout.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            logout(request)

            return HttpResponseRedirect(reverse('index'))



