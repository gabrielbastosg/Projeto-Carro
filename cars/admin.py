from django.contrib import admin
from .models import Car,Favorite
# Register your models here.

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('nome', 'marca', 'preco', 'ano', 'categoria')
    search_fields = ('nome', 'marca')
    list_filter = ('marca', 'categoria', 'combustivel', 'ano')

    fields = (
        'nome', 'marca', 'preco', 'imagem',
        'ano', 'potencia', 'consumo',
        'combustivel', 'categoria', 'descricao'
    )

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'created_at')
    search_fields = ('user__username', 'car__nome')