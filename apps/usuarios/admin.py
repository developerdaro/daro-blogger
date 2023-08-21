from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario,TipoDocumento,Rol

from django.utils.html import format_html


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('imagen_preview','correo', 'rol', 'is_active', 'is_staff','is_superuser')
    list_filter = ('rol','is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('correo', 'password')}),
        ('Informacion personal', {'fields': ('tipo_documento','numero_identificacion','nombre', 'apellido','fecha_nacimiento')}),
        ('Perfil',{'fields':('foto_perfil','slug','groups','archivo_excel')}),
        ('Permisos', {'fields': ('rol','is_active', 'is_staff', 'is_superuser')}),
        # Excluir date_joined de los campos editables
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('tipo_documento','numero_identificacion','nombre', 'apellido','correo', 'password1', 'password2','rol'),
        }),
    )
    ordering = ('correo',)  # Cambia esto al campo deseado para ordenar
    
    def imagen_preview(self, obj):
        if obj.foto_perfil:
            return format_html('<img src="{}" alt="{}" width="50" height="50" />',
                               obj.foto_perfil.url, obj.nombre)
        return 'Sin foto'
    imagen_preview.short_description = 'Imagen de Perfil'



class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    list_filter = ('nombre',)
  
    ordering = ('nombre',)  # Cambia esto al campo deseado para ordenar

class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    list_filter = ('nombre',)
  
    ordering = ('nombre',)  # Cambia esto al campo deseado para ordenar

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(TipoDocumento, TipoDocumentoAdmin)
admin.site.register(Rol, RolAdmin)

from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group

class CustomGroupAdmin(GroupAdmin):
    list_display = ('name', 'get_users_count')

    def get_users_count(self, obj):
        return obj.user_set.count()

    get_users_count.short_description = 'Usuarios en el grupo'

admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)

