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
                return redirect('usuarios:excel')  # Redirige a la página de administrador
            elif user.groups.filter(name='Usuarios_externos').exists():
                return redirect('usuarios:excel')  # Redirige a la página de usuario normal
        else:
            messages.error(request, 'Usuario o contraseña in    correctos.')
    return render(request, 'ingreso/login.html')

def cerrar_sesion(request):
    logout(request)
    return redirect('usuarios:login')

def registro(request):
    return render(request,'ingreso/registro.html')

def perfil(request):
    usuario = request.user

    if request.method == 'POST' and request.FILES:
        archivo_foto = request.FILES['nueva_foto_perfil']
        
        usuario.foto_perfil = archivo_foto
        usuario.save()
        
        return redirect('usuarios:perfil')
    return render(request,'usuarios/perfil.html',{'usuario':usuario})

def inicio(request):
    
    return render(request,'usuarios/inicio.html')



def excel(request):
    if request.method == 'POST' and request.FILES:
        archivo = request.FILES['archivo_excel']
        if archivo.name.endswith('.xlsx'):
            if request.user.is_authenticated:
                request.user.archivo_excel = archivo
                request.user.save()
            df = pd.read_excel(archivo)
            
            # Realizar la operación y crear una nueva columna 'Total'
            df['IVA_VENTA'] = (df['Precio_venta'] * df['IVA'])/100            
            df['UTILIDAD'] = (df['Precio_venta'] - df['Costo'])/df['Costo']
            df['UTILIDAD']=pd.Series([round(val,2) for val in df["UTILIDAD"]])
            df['IVA_VENTA']=pd.Series([round(val,2) for val in df["IVA_VENTA"]])
            df = df.fillna(0)

            data = df.to_dict(orient='records')
            paginator = Paginator(data, 100)  # 10 elementos por página
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'usuarios/excel.html', {'page_obj': page_obj})
    return render(request, 'usuarios/excel.html')