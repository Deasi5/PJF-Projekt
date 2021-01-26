from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from users import views as user_views
app_name = 'myapp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('', views.home, name='home'),
    path('add_product/<int:pk>/', views.add_product, name='add_product'),
    path('remove_product/<int:pk>/', views.remove_product, name='remove_product'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('search_recipes/', views.search_recipes, name='search_recipes'),
    path('search_ingredients/', views.search_ingredients, name='search_ingredients'),
]

for url in urlpatterns:
    print(url)