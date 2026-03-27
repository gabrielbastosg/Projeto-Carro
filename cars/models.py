from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Car(models.Model):
    nome = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='cars/', blank=True, null=True)

    ano = models.IntegerField(null=True, blank=True)
    potencia = models.IntegerField(null=True, blank=True)
    consumo = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    combustivel = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    categoria = models.CharField(
        max_length=50,
        choices=[
            ('SUV', 'SUV'),
            ('SEDAN', 'Sedan'),
            ('HATCH', 'Hatch'),
            ('PICAPE', 'Picape'),
            ('ESPORTE', 'Esportivo'),
        ],
        null=True,
        blank=True
    )

    descricao = models.TextField(null=True, blank=True)

    # =======================
    # 🔥 SCORE CALCULADO
    # =======================
    @property
    def score(self):
        try:
            return (self.potencia / (self.consumo * float(self.preco))) * 10000
        except (TypeError, ZeroDivisionError):
            return 0

    def __str__(self):
        return self.nome


# =======================
# ❤️ FAVORITOS
# =======================
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')

    def __str__(self):
        return f"{self.user.username} - {self.car.nome}"