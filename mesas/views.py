from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from .models import Desk, Reservation
from .forms import ReservationForm
from datetime import date


# -------------------------------------------
# MAPA DO ESCRITÓRIO
# -------------------------------------------
@never_cache
@login_required(login_url='/login/')
def mapa_view(request):
    hoje = date.today()
    mesas = Desk.objects.all()

    # Marca mesas ocupadas hoje
    for mesa in mesas:
        mesa.ocupada = Reservation.objects.filter(
            mesa=mesa,
            data=hoje
        ).exists()

    total = mesas.count()
    ocupadas = sum(1 for m in mesas if m.ocupada)
    livres = total - ocupadas

    porcent_ocupadas = round((ocupadas / total) * 100) if total else 0
    porcent_livres = round((livres / total) * 100) if total else 0

    return render(request, "mesas/mapa.html", {
        "mesas": mesas,
        "ocupadas": ocupadas,
        "livres": livres,
        "porcent_ocupadas": porcent_ocupadas,
        "porcent_livres": porcent_livres,
    })


# -------------------------------------------
# DETALHE DA MESA + CRIAÇÃO DE RESERVA
# -------------------------------------------
@never_cache
@login_required(login_url='/login/')
def mesa_detalhe_view(request, mesa_id):
    mesa = get_object_or_404(Desk, id=mesa_id)
    hoje = date.today()

    reservas = Reservation.objects.filter(
        mesa=mesa,
        data__gte=hoje
    ).order_by("data", "hora_inicio")

    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            nova_reserva = form.save(commit=False)
            nova_reserva.user = request.user
            nova_reserva.mesa = mesa

            # --- Impedir conflito de horário na mesma mesa ---
            conflito = Reservation.objects.filter(
                mesa=mesa,
                data=nova_reserva.data,
                hora_inicio__lt=nova_reserva.hora_fim,
                hora_fim__gt=nova_reserva.hora_inicio,
            ).exists()

            if conflito:
                messages.error(request, "Esta mesa já está reservada neste horário.")
                return redirect("mesa_detalhe", mesa_id=mesa.id)

            # --- Impedir que o usuário reserve mais de uma mesa no mesmo horário ---
            reservado_pelo_usuario = Reservation.objects.filter(
                user=request.user,
                data=nova_reserva.data,
                hora_inicio__lt=nova_reserva.hora_fim,
                hora_fim__gt=nova_reserva.hora_inicio,
            ).exists()

            if reservado_pelo_usuario:
                messages.error(request, "Você já possui uma reserva nesse horário.")
                return redirect("mesa_detalhe", mesa_id=mesa.id)

            # Se passou nas validações, salva
            nova_reserva.save()
            messages.success(request, "Reserva criada com sucesso!")
            return redirect("mesa_detalhe", mesa_id=mesa.id)
    else:
        form = ReservationForm()

    ocupada_hoje = reservas.filter(data=hoje).exists()

    return render(request, "mesas/mesa_detalhe.html", {
        "mesa": mesa,
        "form": form,
        "reservas": reservas,
        "ocupada_hoje": ocupada_hoje,
        "hoje": hoje,
    })


# -------------------------------------------
# CANCELAR RESERVA
# -------------------------------------------
@never_cache
@login_required(login_url='/login/')
def cancelar_reserva_view(request, reserva_id):
    reserva = get_object_or_404(Reservation, id=reserva_id)

    if reserva.user == request.user:
        reserva.delete()
        messages.success(request, "Reserva cancelada!")

    return redirect("mesa_detalhe", mesa_id=reserva.mesa.id)
