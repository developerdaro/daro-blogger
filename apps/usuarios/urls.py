from django.urls import path
from .views import custom_login,registro,cerrar_sesion,perfil

urlpatterns = [
    path('',custom_login,name='login'),
    path('logout/', cerrar_sesion, name='logout'),
    path('registro/',registro,name='registro'),
    path('perfil/',perfil,name='perfil'),
]
