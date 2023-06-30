from django.contrib.auth import views
from django.db import transaction
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView

from registration.forms import SignUpForm
from registration.models import User, IDPinGenerate


# Create your views here.


class Login(views.LoginView):
    template_name = 'registration/login.html'
    first_time_login = False

    def form_valid(self, form):
        user = form.get_user()
        self.first_time_login = user.last_login
        return super(Login, self).form_valid(form)

    def get_success_url(self):
        return super(Login, self).get_success_url()


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        if form.is_valid():
            obj = IDPinGenerate.objects.get(id_pin=form.instance.username)
            form.instance.share_no = obj.share_no
            form.instance.share_price = obj.share_price
            self.object = form.save()
            obj.created_user = self.object
            obj.save()
        return super(SignUp, self).form_valid(form)

    def get_success_url(self):
        return reverse('registration:login')
