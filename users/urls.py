from django.urls import path
from .views import MyRegisterFormView, LoginFormView, DetailView, UsersListView, LogoutView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
app_name = 'users'


urlpatterns = [
    path('register/', MyRegisterFormView.as_view(), name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('login/', csrf_exempt(LoginFormView.as_view()), name="login"),
    path('<int:id>/', login_required(DetailView.as_view()), name='detail'),
    path('', UsersListView.as_view(), name='list')
]