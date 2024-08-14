
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import TemplateView

from .auth_forms import SignUpForm
from django.contrib.auth.models import User

# signup
class SignupView(TemplateView):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'form': SignUpForm()})
    
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = SignUpForm(request.POST)

            if form.is_valid():
                # save user
                form.save()

                return HttpResponseRedirect(reverse('index'))

            return render(request, self.template_name, {'form': form})

# login


# logout



