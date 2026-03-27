from django.shortcuts import render
from .models import Car,Favorite
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404,redirect
# Create your views here.

def lista_carros(request):
    query = request.GET.get('q', '')
    marca = request.GET.get('marca', '')
    categoria = request.GET.get('categoria', '')  # 🔥 AQUI
    ordem = request.GET.get('ordem', '')
    page = request.GET.get('page')

    carros = Car.objects.all().order_by('id')

    # filtro por nome
    if query:
        carros = carros.filter(nome__icontains=query)

    # filtro por marca
    if marca:
        carros = carros.filter(marca=marca)

    # 🔥 filtro por categoria (NO LUGAR CERTO)
    if categoria:
        carros = carros.filter(categoria=categoria)

    # ordenação
    if ordem == 'menor':
        carros = carros.order_by('preco')
    elif ordem == 'maior':
        carros = carros.order_by('-preco')

    # paginação
    paginator = Paginator(carros, 6)
    carros_paginados = paginator.get_page(page)

    marcas = Car.objects.values_list('marca', flat=True).distinct()

    context = {
        'carros': carros_paginados,
        'marcas': marcas,
        'query': query,
        'marca_selecionada': marca,
        'ordem': ordem,
        'categoria_selecionada': categoria  
    }

    return render(request, 'cars/lista_carros.html', context)


def detalhe_carro(request, id):
    carro = Car.objects.get(id=id)
    return render(request, 'cars/detalhe_carro.html', {'carro':carro})


def comparar_carros(request):
    ids = request.GET.getlist('carros')
    carros = Car.objects.filter(id__in=ids).order_by('preco')

    min_price = None
    melhor_carro = None

    if carros:
        min_price = min(carro.preco for carro in carros)

        melhor_carro = max(carros, key=lambda c: c.score) if carros else None

    return render(request, 'cars/comparar_carros.html',{
        'carros':carros,
        'min_price':min_price,
        'melhor_carro':melhor_carro
    })

@login_required
def toggle_favorite(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        car=car
    )

    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True

    return JsonResponse({'favorited': is_favorite})

@login_required
def lista_favoritos(request):
    favoritos = Favorite.objects.filter(user=request.user).select_related('car')

    carros = [fav.car for fav in favoritos]

    return render(request, 'cars/favoritos.html', {
        'carros': carros
    })