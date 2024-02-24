from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view

from apps.user.forms import UserForm, LoginForm, RegisterForm

from rest_framework.generics import (
    get_object_or_404,
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from apps.user.serializers import (
    UserRegisterSerializer,
    UserListSerializer,
    UserInfoSerializer,
)
from apps.user.models import User, SubjectGrade, Album


class UserRegistrationGenericView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                status=status.HTTP_201_CREATED,
                data=serializer.data
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data=serializer.errors
        )


class ListUsersGenericView(ListAPIView):
    # permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserListSerializer

    def get_queryset(self):
        users = User.objects.exclude(
            id=self.request.user.id
        )

        return users

    def get(self, request: Request, *args, **kwargs):
        users = self.get_queryset()

        if not users:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data=[]
            )

        serializer = self.serializer_class(users, many=True)

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )


class UserDetailGenericView(RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = UserInfoSerializer

    def get_object(self):
        user_id = self.kwargs.get("user_id")

        user_obj = get_object_or_404(User, id=user_id)

        return user_obj

    def get(self, request: Request, *args, **kwargs):
        user = self.get_object()

        serializer = self.serializer_class(user)

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    def put(self, request: Request, *args, **kwargs):
        user = self.get_object()

        serializer = self.serializer_class(
            user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                status=status.HTTP_200_OK,
                data=serializer.data
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data=serializer.errors
        )

    def delete(self, request: Request, *args, **kwargs):
        user = self.get_object()

        user.delete()

        return Response(
            status=status.HTTP_200_OK,
            data=[]
        )





def student(request):
    return render(request, 'user/student.html')

def moderator(request):
    return render(request, 'user/moderator.html')


def student_page(request):
    grades = SubjectGrade.objects.all()
    print(grades)
    return render(request, 'user/student.html', {'grades': grades})

@api_view(['POST'])
def create_album(request):
    if request.method == 'POST':
        album_name = request.data.get('name')
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
        new_album = Album(name=album_name, user=user)
        new_album.save()
        return Response({"message": "Альбом успешно создан"}, status=201)
    return Response({"error": "Неверный метод запроса"}, status=400)


def user_form_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('student') if not user.is_moderator else redirect('moderator')
    else:
        form = UserForm()
    return render(request, 'user/user_form.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('student') if not user.is_moderator else redirect('moderator')
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(request, email=user.email, password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                return redirect('student') if not user.is_moderator else redirect('moderator')
    else:
        form = RegisterForm()
    return render(request, 'user/register.html', {'form': form})