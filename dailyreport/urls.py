from django.urls import path
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='dailyreport/login.html'), name='login'),
]
