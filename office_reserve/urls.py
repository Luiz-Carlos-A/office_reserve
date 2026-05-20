from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('contas.urls')),  # <-- LOGIN como página inicial
    path('mesas/', include('mesas.urls')),
]
