from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Order


# Create your views here.


def index_view(request):
    return render(request, 'orders/index.html')


class OrderListView(ListView):
    model = Order
    template_name = 'orders/orders_list.html'


class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
