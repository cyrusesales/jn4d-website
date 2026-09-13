from .models import Cart, Wishlist
from itertools import groupby

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

def topay_item_count(request):
    topay_item_count = 0

    topay_orders = Cart.objects.filter(status='To pay', user_id=request.user.id).order_by('-order_id', 'status')
    #Group cart records by order_id
    grouped_orders = []

    group_key = lambda x: (x.order_id, x.status)

    for (order_id, status), items in groupby(
        topay_orders,
        key=group_key,
    ):
        grouped_orders.append({
            'order_id': order_id,
            'items': list(items),
            'status': status,
        })

    topay_item_count = len(grouped_orders)

    return {
        'topay_item_count': topay_item_count
    }

def toship_item_count(request):
    toship_item_count = 0

    toship_orders = Cart.objects.filter(status='To ship', user_id=request.user.id).order_by('-order_id', 'status')
    #Group cart records by order_id
    grouped_orders = []

    group_key = lambda x: (x.order_id, x.status)

    for (order_id, status), items in groupby(
        toship_orders,
        key=group_key,
    ):
        grouped_orders.append({
            'order_id': order_id,
            'items': list(items),
            'status': status,
        })

    toship_item_count = len(grouped_orders)

    return {
        'toship_item_count': toship_item_count
    }