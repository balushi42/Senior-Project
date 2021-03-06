"""blimp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_simplejwt import views as jwt_views

from core import views as core_views
from library import views as library_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', core_views.profile, name='account_view'),
    path('accounts/signup/', core_views.SignUp.as_view(), name='signup'),
    path('', library_views.home, name='home'),
    path('watch', library_views.video_detail, name='watch'),

    path('api/v1/register/', core_views.CreateUserView.as_view(), name='signup_api'),
    path('api/v1/token/', jwt_views.TokenObtainPairView.as_view(), name='token_auth'),
    path('api/v1/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/videos/', library_views.video_list, name='video_list'),
    re_path(r'api/v1/videos/(?P<pk>[0-9]+)', library_views.video_detail_api, name="video_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)