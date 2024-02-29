from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenRefreshView
)

from apps.user.views import (
    UserDetailGenericView,
    LoginView,
    GetUsersView,
    RegisterView,
    ModeratorView,
    StudentProfileView,
    UserProfileView
)

urlpatterns = [
    path("<int:user_id>/", UserDetailGenericView.as_view()),
    path("auth/refresh-token/", TokenRefreshView.as_view()),

    path('user/<int:user_id>/', UserProfileView.as_view(), name='user_profile'),
    path('moderator/', ModeratorView.as_view(), name='moderator'),
    path('login/', LoginView.as_view(), name='login'),
    path('', RegisterView.as_view(), name='register'),
    path('register/', RegisterView.as_view(), name='register'),
    path('student_profile/', StudentProfileView.as_view(), name='student_profile'),
    path('get_users/', GetUsersView.as_view(), name='get_users'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
