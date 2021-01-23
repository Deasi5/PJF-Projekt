from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Product, Meal
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests
# Create your views here.


@login_required()
def home(request):
    ingredients = loadData()
    food = []
    for ingredient in ingredients['results']:
        food.append(ingredient)

    context = {
        'ingredient': food
    }
    return render(request, 'myapp/home.html', context)


def details(request):
    return render(request, 'myapp/detail.html')


def loadData():
    response = requests.get('https://api.spoonacular.com/food/ingredients/search?apiKey=3ef1f3b4475f4a46a5347c6f8443b2d4&query=chi&number=40')
    return response.json()

# def index(request):
#     product_list = Product.objects.order_by('-product_name')[0:]
#     context = {'product_list': product_list}
#     return render(request, 'myapp/index.html', context)     # render laduje szablon, wypelnia kontekst i zwraca obiekt httpResponse
#
#
# def user(request):
#     return HttpResponse('user')
#
#
# def detail(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     return render(request, 'myapp/detail.html', {'product': product})
#
#
# def choice(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     try:
#         selected_product = product.meal_set.get(pk=request.POST['meal'])
#     except (KeyError, Meal.DoesNotExitst):
#         return render(request, 'myapp/detail.html', {
#             'product': product,
#             'error_message': "You did not select a meal",
#         })
#     else:
#         selected_product.results += 1
#         selected_product.save()
#         return HttpResponseRedirect(reverse('myapp:detail', args=(product.id,)))
#
#
# def results(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     return render(request, 'myapp/results.html', {'product': product})
