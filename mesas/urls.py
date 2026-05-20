from django.urls import path
from . import views

urlpatterns = [
    path("mapa/", views.mapa_view, name="mapa"),
    path("mesa/<int:mesa_id>/", views.mesa_detalhe_view, name="mesa_detalhe"),
    path("cancelar/<int:reserva_id>/", views.cancelar_reserva_view, name="cancelar_reserva"),
]
