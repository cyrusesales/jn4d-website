from .models import Cart, Wishlist

def cart_item_count(request):
    item_count = 0

    if request.user.is_authenticated:
        item_count = Cart.objects.filter(
            user=request.user,
            status='cart'
        ).count()

    return {
        'item_count': item_count
    }

def wish_item_count(request):
    wish_item_count = 0

    if request.user.is_authenticated:
        wish_item_count = Wishlist.objects.filter(
            user=request.user,
            status='wishlist'
        ).count()

    return {
        'wish_item_count': wish_item_count
    }