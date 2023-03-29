from .views import *
from django.urls import path
from django.contrib.auth import views as authViews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='main'),
    path('login/', user_login, name='login'),
    path('exit/', authViews.LogoutView.as_view(next_page='main'), name='exit'),
    path('profile/', profile, name='profile')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)