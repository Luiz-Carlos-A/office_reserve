from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


def logout_custom(request):
    logout(request)
    return redirect('login')


# -------- LOGIN --------
@never_cache
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        user = authenticate(request, username=email, password=senha)

        if user:
            login(request, user)
            return redirect("/home/")
        else:
            return render(request, "contas/login.html", {"erro": "Usuário ou senha incorretos."})

    return render(request, "contas/login.html")


# -------- CADASTRO --------
@never_cache
def cadastro_view(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        senha2 = request.POST.get("senha2")

        if User.objects.filter(username=email).exists():
            return render(request, "contas/cadastro.html", {"erro": "Email já cadastrado."})
        
        if senha != senha2:
            return render(request, "cadastro.html", {
                "erro": "As senhas não coincidem!"
            })

        user = User.objects.create_user(
            username=email,
            first_name=nome,
            email=email,
            password=senha
        )
        user.save()

        return redirect("/login/")

    return render(request, "contas/cadastro.html")


# -------- LOGOUT --------
@never_cache
def logout_view(request):
    logout(request)
    return redirect("/login/")


# -------- HOME (RAIZ DO SITE) --------
# -------- DASHBOARD --------
@never_cache
@login_required(login_url='/login/')
def home_view(request):
    from mesas.models import Desk, Reservation
    from datetime import date

    hoje = date.today()

    # --- DADOS GERAIS ---
    total_mesas = Desk.objects.count()
    ocupadas_hoje = Reservation.objects.filter(data=hoje).count()
    mesas_livres = total_mesas - ocupadas_hoje if total_mesas else 0
    reservas_do_dia = ocupadas_hoje

    # 🔥 NOVO: RESERVAS DO USUÁRIO LOGADO
    reservas = Reservation.objects.filter(
        user=request.user
    ).order_by('-data', '-hora_inicio')

    contexto = {
        "total_mesas": total_mesas,
        "ocupadas_hoje": ocupadas_hoje,
        "mesas_livres": mesas_livres,
        "reservas_do_dia": reservas_do_dia,
        "reservas": reservas,  # 👈 ESSA LINHA É A MAIS IMPORTANTE
    }

    return render(request, "contas/home.html", contexto)


# -------- HOME INTERNA --------
@never_cache
@login_required(login_url='/login/')
def home_page(request):
    return render(request, 'contas/home.html')
