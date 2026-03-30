from .models import Favorite

def favoritos_count(request):
    if request.user.is_authenticated:
        count = Favorite.objects.filter(user=request.user).count()
    else:
        count = 0

    return {
        'favoritos_count': count
    }