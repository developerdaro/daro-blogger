from django.urls import path
from .views import custom_login,registro,cerrar_sesion,perfil,excel,inicio

urlpatterns = [
    path('',custom_login,name='login'),
    path('logout/', cerrar_sesion, name='logout'),
    path('registro/',registro,name='registro'),
    path('perfil/',perfil,name='perfil'),
    path('inicio/',inicio,name='inicio'),
    
    
    
    
    path('excel/',excel,name='excel'),
]
