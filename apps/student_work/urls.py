from django.urls import path
from apps.student_work.views import (
    CreateWorkView,
    DecodeImageView,
    AllStudentWorksView,
    ResponseTextView,
    CreateExampleView,
    DecodeImageExapleView,
    UpdateTextWorkView,
    UpdateProvenTextWorkView,
    UpdateExampleView
)


urlpatterns = [
    path("create/", CreateWorkView.as_view()),
    path("all-work/", AllStudentWorksView.as_view()),
    path("decode/", DecodeImageView.as_view()),
    path("proven/", ResponseTextView.as_view()),
    path("update-text/<int:work_id>/", UpdateTextWorkView.as_view()),
    path("update-proven/<int:work_id>/", UpdateProvenTextWorkView.as_view()),

    path("example/", CreateExampleView.as_view()),
    path("example-decode/", DecodeImageExapleView.as_view()),
    path("update-example/<int:example_id>/", UpdateExampleView.as_view()),

]
