from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import JustificacionForm
from .models import Justificacion

# --- LOGIN ---
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # redirige a tu home
        else:
            return render(request, 'asistencia/login.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'asistencia/login.html')


# --- LOGOUT ---
def logout_view(request):
    logout(request)
    return redirect('login')


# --- HOME ---
@login_required
def home(request):
    return render(request, 'home.html')


# --- JUSTIFICAR INASISTENCIA ---
@login_required
def justificar_inasistencia(request):
    if request.method == 'POST':
        form = JustificacionForm(request.POST, request.FILES)
        if form.is_valid():
            justificacion = form.save(commit=False)
            justificacion.usuario = request.user
            justificacion.save()
            return redirect('historial_justificaciones')
    else:
        form = JustificacionForm()
    return render(request, 'justificar_inasistencia.html', {'form': form})


# --- HISTORIAL ---
@login_required
def historial_justificaciones(request):
    justificaciones = Justificacion.objects.filter(usuario=request.user).order_by('-fecha_envio')
    return render(request, 'historial_justificaciones.html', {'justificaciones': justificaciones})