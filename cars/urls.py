from django.urls import path
from .views import lista_carros,detalhe_carro,comparar_carros,toggle_favorite
from . import views

urlpatterns = [
    path('', lista_carros, name='lista_carros'),
    path('carro/<int:id>/',detalhe_carro,name ='detalhe_carro'),
    path('comparar/', comparar_carros, name='comparar_carros'),
    path('favorito/<int:car_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favoritos/', views.lista_favoritos, name='favoritos'),
]