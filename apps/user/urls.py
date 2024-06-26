from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenRefreshView
)

from apps.user.views import (
    LoginView,
    GetUsersView,
    RegisterView,
    ModeratorView,
    StudentProfileView,
    UserProfileView,
    AdminPageView,
    WorkDeleteView,
    DeleteUserView,
    LogoutView,
    ToggleStatusView,
    AddUserView,
    AllStudentClassView
)

urlpatterns = [
    path("auth/refresh-token/", TokenRefreshView.as_view()),

    path('user/<int:user_id>/', UserProfileView.as_view(), name='user_profile'),
    path('moderator/', ModeratorView.as_view(), name='moderator'),
    path('login/', LoginView.as_view(), name='login'),
    path('', RegisterView.as_view(), name='register'),
    path('register/', RegisterView.as_view(), name='register'),
    path('student_profile/', StudentProfileView.as_view(), name='student_profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('get_users/', GetUsersView.as_view(), name='get_users'),
    path('admin_page/', AdminPageView.as_view(), name='admin_page'),
    path('delete/<int:user_id>/', DeleteUserView.as_view(), name='delete_user'),
    path('delete_work/<int:work_id>/', WorkDeleteView.as_view(), name='delete_work'),
    path('api/toggle-status/', ToggleStatusView.as_view(), name='toggle_status'),
    path('add-user/', AddUserView.as_view(), name='add_user'),
    path('class_user/<int:type_work_id>', AllStudentClassView.as_view(), name='class_user')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
