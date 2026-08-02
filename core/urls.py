from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('analytics/', include('analytics.urls')), # Inclut la sous-application
]
