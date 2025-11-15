from django.contrib import admin
from django.urls import path, include
from EVA import views  # <--- Import corregido

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),  # o la vista principal de tu app
    path('', include('EVA.urls')),  # 👈 enlaza tu app
]
