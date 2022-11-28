"""Django_learning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from .views import home_view
from accounts import views as accounts_views

urlpatterns = [
    path('', home_view, name='home'),
    # path('articles/', include('articles.urls')),
    path('recipes/', include('recipes.urls')),
    path('login/', accounts_views.login_view, name='login'),
    path('logout/', accounts_views.logout_view, name='logout'),
    path('register/', accounts_views.register_view, name='register'),
    path('admin/', admin.site.urls),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
] + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
