from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenRefreshView
)

from apps.user.views import (
    UserRegistrationGenericView,
    ListUsersGenericView,
    UserDetailGenericView, UploadImagesView,
)
from apps.jwt_config.views import (
    CustomTokenObtainPairView
)

urlpatterns = [
    # path("", ListUsersGenericView.as_view()),
    path("<int:user_id>/", UserDetailGenericView.as_view()),
    # path("register/", UserRegistrationGenericView.as_view(), name='register'),
    # path("auth/login/", CustomTokenObtainPairView.as_view()),
    path("auth/refresh-token/", TokenRefreshView.as_view()),

    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
    path('moderator/', views.moderator_view, name='moderator'),
    path('login/', views.login_view, name='login'),
    path('', views.register, name='register'),
    path('register/', views.register, name='register'),
    path('create_work/', views.CreateWorkView.as_view(), name='create_work'),
    path('all_student_works/', views.AllStudentWorksView.as_view(), name='all_student_works'),
    path('student_profile/', views.student_profile, name='student_profile'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

