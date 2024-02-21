from django.urls import path
from apps.student_work.views import (
    CreateWorkView,
    DecodeImageView,
    AllStudentWorksView,
    ResponseTextView
)


urlpatterns = [
    path("create/", CreateWorkView.as_view()),
    path("decode/", DecodeImageView.as_view()),
    path("all_work/", AllStudentWorksView.as_view()),
    path("proven/", ResponseTextView.as_view()),
]
