from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import  Group
from django.utils.text import slugify

class TipoDocumento(models.Model):
    nombre=models.CharField(verbose_name="Nombre", max_length=50)
    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table="usuarios.TipoDocumento"
        verbose_name="Tipo de documentos"
        verbose_name_plural="Tipo de documentos"

class Rol(models.Model):
    nombre=models.CharField(verbose_name="Nombre", max_length=50)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table="usuarios.Rol"
        verbose_name="Rol"
        verbose_name_plural="Roles"


class Usuario(AbstractBaseUser, PermissionsMixin):
    tipo_documento=models.ForeignKey(TipoDocumento,on_delete=models.SET_NULL,null=True,blank=True)
    numero_identificacion=models.IntegerField(unique=True,null=True,blank=True)
    
    correo = models.EmailField(unique=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    
    fecha_nacimiento=models.DateField("Fecha de nacimiento",null=True,blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    archivo_excel = models.FileField(upload_to='archivos_excel/', blank=True, null=True)

    #Acceso
    is_active = models.BooleanField("Habilitado",default=True)
    is_staff = models.BooleanField("Acceso al admin",default=False)
    
    #Relaciones
    rol=models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True,blank=True, default=2)

    foto_perfil=models.ImageField('Foto de perfil', upload_to='usuario/perfil', null=True,blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['numero_identificacion','nombre','apellido']

    def __str__(self):
        return self.correo
    
    class Meta:
        db_table="usuarios.Usuario"
        verbose_name="Usuario"
        verbose_name_plural="Usuarios"

    def save(self, *args, **kwargs):
        if not self.slug:
            campos_para_slug = f"{self.nombre} {self.apellido}"  # Concatenar los campos deseados
            self.slug = self.generate_unique_slug(campos_para_slug)
        super().save(*args, **kwargs)

    def generate_unique_slug(self, campos_para_slug):
        slug = slugify(campos_para_slug)
        nuevo_slug = slug
        contador = 1

        while Usuario.objects.filter(slug=nuevo_slug).exclude(id=self.id).exists():
            nuevo_slug = f"{slug}-{contador}"
            contador += 1
        
        return nuevo_slug
        
    def asignar_grupo(self):
        grupo = Group.objects.get(name='Usuarios_externos')
        self.groups.add(grupo)
        
@receiver(post_save, sender=Usuario)
def asignar_grupo_usuario(sender, instance, created, **kwargs):
    if created:
        instance.asignar_grupo()




