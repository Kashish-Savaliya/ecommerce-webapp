"""
URL configuration for ecomweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('shop.urls')),
    path('blog/', include('blog.urls')),
    path('', views.index)
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# settings.MEDIA_URL: This is the URL endpoint where media files are expected to be served from. It's typically defined in the Django project settings (settings.py).
# settings.MEDIA_ROOT: This is the filesystem path where uploaded media files are stored. It's also defined in the Django project settings.
# static(): This function is used to serve static files during development. Here, it's being used to serve media files because media files are essentially static files that need to be served.
# The static() function dynamically adds this URL pattern to the project's URL patterns when the DEBUG setting is set to True.
# This allows Django to serve media files directly during development.