from django.contrib import admin
from django.urls import include, path
from django.views.defaults import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('account.urls')),
    path('finance/', include('finance.urls')),
    path('', include('dashboard.urls')),
]

handler404 = lambda request, exception: page_not_found(request, exception, template_name='404.html')
