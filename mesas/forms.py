from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["data", "hora_inicio", "hora_fim"]
        widgets = {
            "data": forms.DateInput(attrs={"type": "date"}),
            "hora_inicio": forms.TimeInput(attrs={"type": "time"}),
            "hora_fim": forms.TimeInput(attrs={"type": "time"}),
        }
