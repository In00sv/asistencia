from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Modelo personalizado de usuario
class Usuario(AbstractUser):
    ROLES = [
        ('estudiante', 'Estudiante'),
        ('validador', 'Validador'),
        ('receptor', 'Receptor'),
    ]
    rol = models.CharField(max_length=20, choices=ROLES, default='estudiante')
    rut = models.CharField(max_length=12, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.rol})"


# Modelo de asistencia
class Asistencia(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='Presente')

    def __str__(self):
        return f"{self.usuario.username} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"


class Justificacion(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_inasistencia = models.DateField()
    motivo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    documento = models.FileField(upload_to='justificaciones/', blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')
    comentarios_validador = models.TextField(blank=True, null=True)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.fecha_inasistencia} ({self.estado})"