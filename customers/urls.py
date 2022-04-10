from django.urls import path
from . import views

app_name = "customers"

urlpatterns = [
    path('', views.home, name='home'),
    # path('users/sign_up', views.register, name='sign_up'),
    # path('login', views.login_user, name='login'),
    # path('logout', views.logout_request, name='logout'),
    # path('customers', views.customers_list, name='customers_list'),
    path('customers', views.client_list, name='clients_list'),
    path('settings', views.settings, name='settings'),
    path('services', views.services, name='services'),
    path('customers/new', views.customers_create, name='customers_create'),
    path('suppliers', views.suppliers_list, name='suppliers_list'),
    path('suppliers/new', views.suppliers_create, name='suppliers_create'),
    # path('passwords/new', views.password_reset, name='password_reset'),
    path('client_create/new', views.client_create, name='client_create'),
    path('client_detail/<int:id>/', views.client_detail, name='client_detail'),
    path('contact_create/', views.contact_create, name='contact_create'),
    path('note_create/', views.note_create, name='note_create'),
    path('team_members/', views.team_members, name='team_members'),
]
