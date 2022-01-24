import json
from django.shortcuts import redirect, render
from django.template import context
from .models import Pizza, Order
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def home(request):
    pizzas=Pizza.objects.all()
    orders=Order.objects.all()
    context={'pizzas':pizzas, 'orders':orders}
    return render(request, "home.html", context)

def order(request, order_id):
    order=Order.objects.filter(order_id=order_id).first()
    if not order:
        return redirect('/')
    else:
        context={'order':order}
        return render(request, 'order.html',context )

@csrf_exempt
def order_pizza(request):
    user=request.user
    data=json.loads(request.body)
    try:
        pizza=Pizza.objects.get(id=data.get('id'))
        order=Order(pizza=pizza, user=user, amount=pizza.price)
        order.save()
        return JsonResponse({'success':"true"})
    except Pizza.DoesNotExist:
        return JsonResponse({"error":"something went worng","sucess":"false"})