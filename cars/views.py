from django.shortcuts import render
from .models import Car,Favorite
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.forms import UserCreationForm
import os
import requests

# Create your views here.

def lista_carros(request):
    query = request.GET.get('q', '')
    marca = request.GET.get('marca', '')
    categoria = request.GET.get('categoria', '')  
    ordem = request.GET.get('ordem', '')
    page = request.GET.get('page')

    carros = Car.objects.all().only(
        'id', 'nome', 'marca', 'preco', 'imagem', 
        'categoria', 'combustivel', 'potencia', 'consumo'
    ).order_by('id')

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
    elif ordem == 'score':
        carros = sorted(carros, key=lambda c: c.score, reverse=True)
    
    # Numero de favoritos
    favoritos_count = 0

    if request.user.is_authenticated:
        favoritos_count = Favorite.objects.filter(user=request.user).count()

    # paginação
    paginator = Paginator(carros, 6)
    carros_paginados = paginator.get_page(page)

    melhor_carro = None

    if carros_paginados:
        melhor_carro = max(carros_paginados, key=lambda c: c.score)

    marcas = Car.objects.values_list('marca', flat=True).distinct()

    context = {
        'carros': carros_paginados,
        'marcas': marcas,
        'query': query,
        'marca_selecionada': marca,
        'ordem': ordem,
        'categoria_selecionada': categoria ,
        'melhor_carro': melhor_carro, 
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

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


def buscar_carros_api(request):
    make = request.GET.get("make", "")

    url = f"https://api.api-ninjas.com/v1/cars?make={make}"
    headers = {"X-Api-Key": os.getenv("API_NINJAS_KEY")}

    try:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return JsonResponse([], safe=False)

        data = response.json()

        carros_formatados = []

        for car in data:
            carros_formatados.append({
                "make": car.get("make", "").title(),
                "model": car.get("model", "").title(),
                "year": car.get("year", "N/A"),
                "fuel_type": car.get("fuel_type", "N/A"),
                "image_url": "/static/cars/default_car.png"
            })

        return JsonResponse(carros_formatados, safe=False)

    except:
        return JsonResponse([], safe=False)

def testar_api(request):
    url = "https://api.api-ninjas.com/v1/cars?make=toyota"
    headers = {"X-Api-Key": os.getenv("API_NINJAS_KEY")}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return JsonResponse({
            "erro": "API em manutenção ou chave inválida",
            "status": response.status_code
        }, status=500)

    try:
        data = response.json()
    except:
        return JsonResponse({"erro": "Erro ao converter JSON"})

    return JsonResponse(data, safe=False)