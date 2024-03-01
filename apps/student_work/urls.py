from django.urls import path
from apps.student_work.views import (
    CreateWorkView,
    AllStudentWorksView,
    ResponseTextView,
    CreateExampleView,
    UpdateProvenTextWorkView,
    UpdateExampleView,
    ExampleCreateView,
    DecodeImageExapleView
)


urlpatterns = [
    path("create/", CreateWorkView.as_view(), name='create-work'),
    path("all-work/", AllStudentWorksView.as_view(), name='all-work'),
    path("proven/<int:work_id>/", ResponseTextView.as_view(), name='check-work'),
    path("update-proven/<int:work_id>/", UpdateProvenTextWorkView.as_view(), name='update-work'),

    path("example/", CreateExampleView.as_view()),
    path('example/create/', ExampleCreateView.as_view(), name='create_example'),
    path('decode_image/<int:example_id>/', DecodeImageExapleView.as_view(), name='decode_image'),
    path("update-example/<int:example_id>/", UpdateExampleView.as_view(), name='update-example'),
]
