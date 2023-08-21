from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
import pandas as pd
from django.core.paginator import Paginator

from django.contrib.auth import logout


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.groups.filter(name='Usuarios_Internos').exists():
                return redirect('usuarios:perfil')  # Redirige a la página de administrador
            elif user.groups.filter(name='Usuarios_externos').exists():
                return redirect('usuarios:perfil')  # Redirige a la página de usuario normal
        else:
            messages.error(request, 'Usuario o contraseña in    correctos.')
    return render(request, 'ingreso/login.html')

def cerrar_sesion(request):
    logout(request)
    return redirect('usuarios:login')

def registro(request):
    return render(request,'ingreso/registro.html')

def perfil(request):
    if request.method == 'POST' and request.FILES:
        archivo = request.FILES['archivo_excel']
        if archivo.name.endswith('.xlsx'):
            if request.user.is_authenticated:
                request.user.archivo_excel = archivo
                request.user.save()
            df = pd.read_excel(archivo)
            
            # Realizar la operación y crear una nueva columna 'Total'
            df['IVA_VENTA'] = (df['Precio_venta'] * df['IVA'])/100
            df['UTILIDAD'] = (df['Precio_venta'] * df['IVA'])/100
            
            data = df.to_dict(orient='records')
            paginator = Paginator(data, 100)  # 10 elementos por página
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'usuarios/perfil.html', {'page_obj': page_obj})
    return render(request, 'usuarios/perfil.html')