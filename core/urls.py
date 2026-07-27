from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('admin/', permanent=False)),
    path('admin/', admin.site.urls),
]
