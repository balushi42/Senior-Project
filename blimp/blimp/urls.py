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
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_simplejwt import views as jwt_views

from core import views as core_views
from library import views as library_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/register/', core_views.CreateUserView.as_view(), name='signup_api'),
    path('api/v1/token/', jwt_views.TokenObtainPairView.as_view(), name='token_auth'),
    path('api/v1/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/me/', core_views.profile_api, name='profile_api'),
    path('api/v1/people/', core_views.people_api, name='people_api'),
    re_path(r'api/v1/people/(?P<pk>[0-9]+)/', core_views.people_detail_api, name="people_detail_api"),
    path('api/v1/friends/', core_views.friends_api, name='friends_api'),
    path('api/v1/friends/pending/', core_views.friends_pending_api, name='friends_pending_api'),

    path('api/v1/videos/', library_views.video_list, name='video_list'),
    re_path(r'api/v1/videos/(?P<pk>[0-9]+)/', library_views.video_detail_api, name="video_detail"),
    re_path(r'api/v1/reactions/(?P<pk>[0-9]+)/', library_views.video_reactions_api, name="video_reactions"),
    path('api/v1/videos/upload/', library_views.video_upload_api, name='video_upload'),

    path('api/v1/timeline/', library_views.timeline_api, name='timeline_api'),

    path('api/v1/categories/', library_views.category_list, name='category_list'),
    re_path(r'api/v1/categories/(?P<pk>[0-9]+)/', library_views.category_detail, name="category_detail"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)