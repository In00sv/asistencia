from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Justificacion
from datetime import date
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile


User = get_user_model()

class TestJustificacionModel(TestCase):

    def test_crear_justificacion(self):
        user = User.objects.create_user(username='test', password='1234')

        just = Justificacion.objects.create(
            usuario=user,
            fecha_inasistencia=date.today(),
            motivo="Enfermedad"
        )

        self.assertEqual(just.usuario.username, "test")
        self.assertEqual(just.estado, "pendiente")


class ModeloJustificacionTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='1234')

    def test_crear_justificacion_modelo(self):
        just = Justificacion.objects.create(
            usuario=self.user,
            fecha_inasistencia=date.today(),
            motivo="Enfermedad"
        )
        self.assertEqual(just.usuario.username, "user1")
        self.assertEqual(just.estado, "pendiente")


class VistaJustificacionTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='userA', password='pass123')

    def test_crear_justificacion(self):
        self.client.login(username='userA', password='pass123')

        data = {
            'fecha_inasistencia': '2024-02-10',
            'motivo': 'Problema médico'
        }

        response = self.client.post(reverse('justificar_inasistencia'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Justificacion.objects.count(), 1)



    def test_ver_historial(self):
        self.client.login(username='userA', password='pass123')

        Justificacion.objects.create(
            usuario=self.user,
            fecha_inasistencia=date.today(),
            motivo="Prueba"
        )

        response = self.client.get(reverse('historial_justificaciones'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Prueba")


class ArchivoPDFTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='userFile', password='1234')

    def test_subir_pdf_correcto(self):
        self.client.login(username='userFile', password='1234')

        pdf = SimpleUploadedFile("doc.pdf", b"contenido de prueba", content_type="application/pdf")

        data = {
            'fecha_inasistencia': '2024-01-01',
            'motivo': 'Documento',
            'documento': pdf,
        }

        response = self.client.post(reverse('justificar_inasistencia'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Justificacion.objects.count(), 1)


    def test_rechazar_archivo_no_pdf(self):
        self.client.login(username='userFile', password='1234')

        archivo_malo = SimpleUploadedFile("virus.exe", b"malicioso", content_type="application/octet-stream")

        data = {
            'fecha_inasistencia': '2024-01-01',
            'motivo': 'Documento',
            'documento': archivo_malo,
        }

        response = self.client.post(reverse('justificar_inasistencia'), data)
        
        # No crea nada
        self.assertEqual(Justificacion.objects.count(), 0)

        # Confirma que hubo error
        self.assertEqual(response.status_code, 200)

class PermisosTests(TestCase):

    def test_historial_sin_login(self):
        response = self.client.get(reverse('historial_justificaciones'))
        self.assertEqual(response.status_code, 302)  # redirección al login


class SeguridadSQLTests(TestCase):

    def setUp(self):
        User.objects.create_user(username='seguro', password='1234')

    def test_login_sql_injection(self):
        response = self.client.post(reverse('login'), {
            'username': "seguro' OR '1'='1",
            'password': "1234"
        })
        self.assertContains(response, "incorrectos")



class IntegracionCompletaTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='integro', password='test123')

    def test_flujo_completo(self):
        # Login
        self.client.login(username='integro', password='test123')

        # Crear justificación
        response1 = self.client.post(reverse('justificar_inasistencia'), {
            'fecha_inasistencia': '2024-02-01',
            'motivo': 'Integración'
        })

        # Ver historial
        response2 = self.client.get(reverse('historial_justificaciones'))

        self.assertEqual(response1.status_code, 302)
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, 'Integración')
