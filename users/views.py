from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import FormView
from .forms import MyForm, ImageForm
from django.contrib.auth import login, logout
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile


class UsersListView(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'users/list.html', {'users': users})


class DetailView(View):
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        form = ImageForm()
        if user.id == request.user.id:
            return render(request, 'users/detail.html', {'user': user, 'form': form})
        else:
            return render(request, 'users/error.html')

    def post(self, request, id):
        user = get_object_or_404(User, id=id)
        form = ImageForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
        return render(request, 'users/detail.html', {'user': user, 'form': form})


class MyRegisterFormView(FormView):
    form_class = MyForm

    success_url = "/login/"

    template_name = "users/register.html"

    def form_valid(self, form):
        new_user = form.save()
        send_mail('Регистрация', 'Поздравляем, вы успешно зарегестрировались на сайте.', \
                  settings.EMAIL_HOST_USER, ['akhtyrtsev@gmail.com'])
        profile = Profile.objects.create(user=new_user)
        return super(MyRegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(MyRegisterFormView, self).form_invalid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm

    template_name = "users/login.html"

    success_url = "/users/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return HttpResponseRedirect(reverse('users:detail', args=[self.request.user.id]))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")

