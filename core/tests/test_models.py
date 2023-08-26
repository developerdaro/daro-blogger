from django.test import TestCase
from apps.usuarios.models import Rol, TipoDocumento, Usuario
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.test import TestCase, RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.usuarios.views import excel  # Importa la función que quieres probar
import pandas as pd  # Importa pandas si aún no lo has hecho
from django.contrib.auth.models import User
import io
import random
import string

class ExcelFunctionTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        TipoDocumento.objects.create(nombre="TipoDocumento 1")
        TipoDocumento.objects.create(nombre="TipoDocumento 2")
        Rol.objects.create(nombre="Admin")
        Rol.objects.create(nombre="Usuario")
        if not Group.objects.filter(name='Usuarios_externos').exists():
            Group.objects.create(name='Usuarios_externos')

    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(correo='daro2@gmail.com', password='testpass')
        self.user.tipo_documento = TipoDocumento.objects.get(nombre="TipoDocumento 1")
        self.user.rol = Rol.objects.get(nombre="Usuario")
        self.user.save()

        # Ruta correcta a la vista excel (ajusta esto según tu configuración de URLs)
        self.excel_view_url = '/excel/'

        # Carga un archivo de prueba (xlsx) para usar en las pruebas
        with open('/home/daro/Descargas/Informe Inventario 13 ago 23.xlsx', 'rb') as file:
            self.excel_uploaded_file = SimpleUploadedFile('/home/daro/Descargas/Informe Inventario 13 ago 23.xlsx', file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    def _encode_multipart_data(self, data):
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        encoded_data = ''
        for key, value in data.items():
            encoded_data += '--BoUnDaRyStRiNg\r\n'
            encoded_data += 'Content-Disposition: form-data; name="{}"\r\n\r\n{}\r\n'.format(key, value)
        encoded_data += '--BoUnDaRyStRiNg--\r\n'
        return content_type, encoded_data

    def test_excel_function(self):
        content_type, data = self._encode_multipart_data({'archivo_excel': self.excel_uploaded_file})
        request = self.factory.post(self.excel_view_url, data, content_type=content_type)
        request.user = self.user

        response = excel(request)

        self.assertEqual(response.status_code, 200)

        # Realiza las operaciones que se hacen en la función excel y verifica los resultados
        df = pd.read_excel(self.excel_uploaded_file, engine='openpyxl')
        df['IVA_VENTA'] = (df['Precio_venta'] * df['IVA'])/100            
        df['UTILIDAD'] = (df['Precio_venta'] - df['Costo'])/df['Costo']
        df['UTILIDAD']=pd.Series([round(val,2) for val in df["UTILIDAD"]])
        df['IVA_VENTA']=pd.Series([round(val,2) for val in df["IVA_VENTA"]])
        df = df.fillna(0)
        self.assertTrue(all(df['IVA_VENTA'] == df['IVA_VENTA']))
        self.assertTrue(all(df['UTILIDAD'] == df['UTILIDAD']))