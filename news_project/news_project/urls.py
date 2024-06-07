
from django.urls import path, include
# urls.py
from django.contrib import admin
from news.views import custom_logout

admin.site.site_header='Finnews'
admin.site.site_title= 'Quản lý hệ thống'
admin.site.index_title ='Quản lý hệ thống'
urlpatterns = [
    #path('dashboard/', include('dashboard.urls')),
    path('admin/dashboard/', include('dashboard.urls')),
    path('admin/', admin.site.urls),
    #path('admin/dashboard/', include('dashboard.urls')),
    #path('admin/', admin_site.urls),
    path('logout/', custom_logout, name='admin_logout'),
    path('api/', include('news.urls')),  
    path('dashboard/', include('dashboard.urls')),



]


