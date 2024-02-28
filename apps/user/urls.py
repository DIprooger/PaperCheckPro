from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenRefreshView
)

from apps.user.views import (
    UserDetailGenericView,
    GetUsersView
)

urlpatterns = [
    path("<int:user_id>/", UserDetailGenericView.as_view()),
    path("auth/refresh-token/", TokenRefreshView.as_view()),

    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
    path('moderator/', views.moderator_view, name='moderator'),
    path('login/', views.login_view, name='login'),
    path('', views.register, name='register'),
    path('register/', views.register, name='register'),
    path('student_profile/', views.student_profile, name='student_profile'),
    path('get_users/', GetUsersView.as_view(), name='get_users'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
