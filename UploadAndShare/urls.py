"""UploadAndShare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views
from django.contrib.auth import views as auth_views
from django.shortcuts import HttpResponseRedirect

urlpatterns = [
    path('favicon.ico/', lambda x: HttpResponseRedirect(settings.STATIC_URL + 'favicon.ico'), name='favicon'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('delete/', core_views.delete_document, name='delete_document'),
    path('select-document/', core_views.share_document, name='select_document'),
    path('save/', core_views.save_shared_document, name='save_shared_documents'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)