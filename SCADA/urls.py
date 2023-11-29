from django.contrib import admin
from django.urls import path
from dailyreport import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('upload_excel/', views.upload_excel, name='upload_excel'),
    path('login/', LoginView.as_view(template_name='dailyreport/login.html'), name='login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('export_to_text_fir/', views.export_to_text_fir, name='export_to_text_fir'),
    path('export_to_text/', views.export_to_text, name='export_to_text'),
    path('export_dailymu_to_text/', views.export_dailymu_to_text, name='export_dailymu_to_text'),
]

