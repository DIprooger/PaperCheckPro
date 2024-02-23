from django.urls import path
from . import views


from rest_framework_simplejwt.views import (
    TokenRefreshView
)

from apps.user.views import (
    UserRegistrationGenericView,
    ListUsersGenericView,
    UserDetailGenericView,
)
from apps.jwt_config.views import (
    CustomTokenObtainPairView
)

urlpatterns = [
    path("", ListUsersGenericView.as_view()),
    path("<int:user_id>/", UserDetailGenericView.as_view()),
    # path("register/", UserRegistrationGenericView.as_view()),
    path("auth/login/", CustomTokenObtainPairView.as_view()),
    path("auth/refresh-token/", TokenRefreshView.as_view()),

    path('student/', views.student, name='student'),
    path('moderator/', views.moderator, name='moderator'),
    path('student/', views.student_page, name='student_page'),
    path('api/create_album/', views.create_album, name='create_album'),
    path('user_form/', views.user_form_view, name='user_form'),
    path('login/', views.login_view, name='login'),

]

