
from django.urls import path, include
# urls.py
from django.contrib import admin
from news.views import custom_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', custom_logout, name='admin_logout'),
    path('api/', include('news.urls')),  
]


