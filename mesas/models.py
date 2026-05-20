from django.db import models
from django.contrib.auth.models import User

class Desk(models.Model):
    nome = models.CharField(max_length=50)
    pos_x = models.IntegerField()
    pos_y = models.IntegerField()
    ocupada = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Desk, on_delete=models.CASCADE)
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    def __str__(self):
        return f"{self.user.username} reservou {self.mesa.nome} em {self.data}"

