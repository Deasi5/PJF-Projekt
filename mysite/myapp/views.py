from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Product, ProductListEntry, Nutrient
from django.urls import reverse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import requests
#from .mock import mock

# Create your views here.
import json
API_KEY = 'apiKey=94e5fa23563543108f33973794b71eb8'
DATA_URL = f'https://api.spoonacular.com/food/ingredients/search?{API_KEY}&query=a&number=20'
IMAGE_URL = 'https://spoonacular.com/cdn/ingredients_250x250/'
RECIPES_URL=f'https://api.spoonacular.com/recipes/findByIngredients?{API_KEY}&ingredients='
SEARCH_URL = 'https://api.spoonacular.com/food/ingredients/search?apiKey=94e5fa23563543108f33973794b71eb8&query='
AMOUNT = 100
DETAIL_KEYS = ['Protein', 'Fat' , 'Carbohydrates']


def data_to_products(data)->list:
    if not (results:=data.get('results',None)):
        return []

    products = []
    for result in results:
        if not (api_id:=result.get('id', None)):
            return []
        product,_=Product.objects.get_or_create(api_id=api_id)
        product.name =result['name']
        product.image_name=result['image']
        products.append(product)
    return products

def get_data()->dict:
    response = requests.get(DATA_URL)
    data = response.json()
    return data

@login_required()
def home(request, *args, **kwargs):
    if not (data:=request.session.get('data',None)):
        # data = mock
        data = get_data()

    products = data_to_products(data)
    list_entries = ProductListEntry.objects.filter(user=request.user)
    #entries = ProductListEntry.objects.filter(user=request.user)    
    #for product, entry in zip(products, entries):                   
    #    entry.product = product                                     
    context = {
        'products': products,
        'list_entries': list_entries
    #    'entries': entries                                         
    }
    return render(request, 'myapp/home.html', context)

def search_ingredients(request, *args, **kwargs):
    search_string = request.GET.get('search_string', '')
    if search_string:
        url = f'{SEARCH_URL}{search_string}'
        response = requests.get(url)
        data = response.json()
        request.session['data'] = data
    else:
        request.session['data'] = None
    return redirect('myapp:home')


def detail(request, *args, **kwargs):
    api_id = kwargs['pk']
    product = Product.objects.filter(api_id=api_id).first()
    if not Nutrient.objects.filter(product__api_id=api_id).exists():
        product, nutrients = fetch_details(api_id, product) 
    else:
        product = Product.objects.filter(api_id=api_id).first()
        nutrients = Nutrient.objects.filter(product=product)

    context={
        'product':product,
        'image':f'{IMAGE_URL}/{product.image_name}'
    }
    return render(request, 'myapp/detail.html', context)

def add_product(request, *args, **kwargs):
    api_id = kwargs['pk']
    product = Product.objects.filter(api_id=api_id).first()
    ProductListEntry.objects.get_or_create(user=request.user, product=product)
    return redirect('myapp:home')

def remove_product(request, *args, **kwargs):
    api_id = kwargs['pk']
    ProductListEntry.objects.filter(product__api_id=api_id).delete()
    return redirect('myapp:home')

def search_recipes(request):
    product_list = ProductListEntry.objects.filter(user=request.user)
    product_names = ',+'.join(list(map(lambda entry: entry.product.name.replace(' ', '%20'),product_list)))

    headers = {
        'Content-Type': 'application/json'
    }
    url = f'{RECIPES_URL}{product_names}'
    response = requests.get(url, headers=headers)
    data = response.json()

    recipes = [{
        'title': recipe.get('title', 'API provides no title'),
        'image' : recipe.get('image', None),
        'missed_ingredients' : [name.get('original',None) for name in recipe.get('missedIngredients',[])]
        } for recipe in data 
    ]

    context = {
        'recipes':recipes,
        'products': [entry.product for entry in product_list]
    }
    return render(request, 'myapp/recipes.html', context=context)

def fetch_details(api_id, product):
    details_url = f'https://api.spoonacular.com/food/ingredients/{api_id}/information{API_KEY}&amout={AMOUNT}'
    details_response = requests.get(details_url)
    data = details_response.json()

    nutrients =[]
    for details in data.get('nutrition',{}).get('nutrients',{}):
        if details['name'] in DETAIL_KEYS:
            nutrient, n_created = Nutrient.objects.get_or_create(product=product).update(**details)
            nutrients.append(nutrient)

    return product, nutrients