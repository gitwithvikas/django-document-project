from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

# from rest_framework.routers import DefaultRouter

# from .views import UserViewSet, UserProfileViewSet

# router = DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'profiles', UserProfileViewSet)

from . import views

urlpatterns = [
    # path('', include(router.urls)),
    path('register/', views.register, name='register'),
    path('login/',views.login,name='login'),
    path('uploadDoc/',views.uploadDoc, name='uploadDoc'),
    path('download/', views.download_documents, name='download_documents'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
