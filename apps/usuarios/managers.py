from django.contrib.auth.models import BaseUserManager
from django.utils.crypto import get_random_string

class CustomUserManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError("The correo field must be set")
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)

        if password:
            user.set_password(password)
        else:
            password = get_random_string()  # Genera una contraseña aleatoria si no se proporciona

        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # Obtén una instancia válida del modelo Rol (supongamos que el rol de administrador tiene ID 1)
        from .models import Rol
        admin_rol = Rol.objects.get(pk=1)
        
        extra_fields.setdefault('rol',admin_rol)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(correo, password, **extra_fields)
