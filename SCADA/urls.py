from django.contrib import admin
from django.urls import path
from dailyreport import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('upload_excel/', views.upload_excel, name='upload_excel'),
    path('upload_excel/', views.upload_excel, name='upload_excel'),
    path('generating_station/update/<int:pk>/', views.update_generating_station, name='update_generating_station'),
    path('grid_frequency/', views.grid_frequency, name='grid_frequency'),
    path('pump_station/', views.pump_station, name='pump_station'),
    path('pump_station/update/<int:pk>/', views.update_pump_station, name='update_pump_station'),
    path('demand_data/', views.demand_data, name='demand_data'),
    path('pump_load_data/', views.pump_load_data, name='pump_load_data'),
    path('state/', views.state, name='state'),
    path('schdrwl_data/', views.schdrwl_data, name='schdrwl_data'),
    path('login/', LoginView.as_view(template_name='dailyreport/login.html'), name='login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('export_to_text/', views.export_to_text, name='export_to_text'),
]
