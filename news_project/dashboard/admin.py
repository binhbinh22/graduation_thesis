# Dashboard/admin.py
from django.contrib import admin
from .models import Dashboard

admin.site.register(Dashboard)


# from django.contrib import admin
# from django.urls import reverse
# from django.http import HttpResponseRedirect
# from django.contrib.admin import AdminSite
# from django.urls import path

# class CustomAdminSite(AdminSite):
#     site_header = "News Project Admin"
#     site_title = "News Admin Portal"
#     index_title = "Welcome to the News Admin Portal"

#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('dashboard/', self.admin_view(self.dashboard_view), name='admin-dashboard'),
#         ]
#         return custom_urls + urls

#     def index(self, request, extra_context=None):
#         extra_context = extra_context or {}
#         extra_context['dashboard_link'] = reverse('admin-dashboard')
#         return super().index(request, extra_context=extra_context)

#     def dashboard_view(self, request):
#         return HttpResponseRedirect('/admin/dashboard/dashboard/')  # Chuyển hướng đến trang dashboard của admin

# admin_site = CustomAdminSite(name='custom_admin')

# admin.site = admin_site  # Ghi đè admin site mặc định bằng admin site tùy chỉnh của chúng ta
