from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import home_view, cadastro_view

urlpatterns = [
    # LOGIN como página inicial
    path('', LoginView.as_view(template_name='contas/login.html'), name='login'),

    # LOGIN usado pelo Django para redirecionar com ?next=
    path('login/', LoginView.as_view(template_name='contas/login.html'), name='login_forced'),

    # HOME após login
    path('home/', home_view, name='home'),

    # CADASTRO
    path('cadastro/', cadastro_view, name='cadastro'),

    # LOGOUT
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
