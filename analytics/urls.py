from django.urls import path
from .views import CADashboardView

urlpatterns = [
    path('dashboard/', CADashboardView.as_view(), name='dashboard_ca'),
]
