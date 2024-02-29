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
    path("create/", CreateWorkView.as_view(), name='create-work'),
    path("all-work/", AllStudentWorksView.as_view(), name='all-work'),
    path("decode/", DecodeImageView.as_view()),
    path("proven/<int:work_id>/", ResponseTextView.as_view(), name='check-work'),
    path("update-text/<int:work_id>/", UpdateTextWorkView.as_view()),
    path("update-proven/<int:work_id>/", UpdateProvenTextWorkView.as_view(), name='update-proven'),

    path("example/", CreateExampleView.as_view()),
    path("example-decode/", DecodeImageExapleView.as_view()),
    path("update-example/<int:example_id>/", UpdateExampleView.as_view()),

]
