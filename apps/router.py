from django.urls import include, path

urlpatterns = [
    path('users/', include('apps.user.urls')),
<<<<<<< HEAD
=======
    path('work/', include('apps.student_work.urls'))
>>>>>>> 6299b8096e3acc9a2793a24f20d863ef5e5c9ad9
]
