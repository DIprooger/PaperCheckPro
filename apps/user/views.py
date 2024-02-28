from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from apps.user.forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm

from django.shortcuts import render

from rest_framework.generics import (
    get_object_or_404,
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.request import Request

from apps.user.serializers import (
    UserRegisterSerializer,
    UserListSerializer,
    UserInfoSerializer
)
from apps.user.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Проверяем статус пользователя и перенаправляем его соответственно
            if user.is_moderator:
                return redirect(reverse('moderator'))
            else:
                return redirect(reverse('student_profile'))
        else:
            # Обработка неудачной попытки входа
            form = AuthenticationForm()
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.is_moderator:
                return redirect('moderator')
            else:
                return redirect('student_profile')
    else:
        form = RegisterForm()
    return render(request, 'user/register.html', {'form': form})


def moderator_view(request):
    # Получаем всех пользователей, которые не являются модераторами или админами
    users = User.objects.filter(is_moderator=False, is_superuser=False)
    return render(request, 'user/moderator.html', {'users': users})


def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user.is_moderator or user.is_superuser:
        return redirect(f'/user/{user_id}/?error=access_denied')

    return render(request, 'user/user_profile.html', {'user': user})


@login_required
def student_profile(request):
   return render(request, 'user/student_profile.html', {'profile': user_profile})


class GetUsersView(View):
    def get(self, request, *args, **kwargs):
        user_ids = request.GET.get('users', '').split(',')
        users = User.objects.filter(id__in=user_ids)
        user_list = [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name} for user in users]
        return JsonResponse(user_list, safe=False)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Проверяем статус пользователя и перенаправляем его соответственно
            if user.is_moderator:
                return redirect(reverse('moderator'))
            else:
                return redirect(reverse('student_profile'))
        else:
            # Обработка неудачной попытки входа
            form = AuthenticationForm()
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.is_moderator:
                return redirect('moderator')
            else:
                return redirect('student_profile')
    else:
        form = RegisterForm()
    return render(request, 'user/register.html', {'form': form})


@login_required
def student_profile(request):
   return render(request, 'user/student_profile.html', {'profile': user_profile})


def moderator_view(request):
    # Получаем всех пользователей, которые не являются модераторами или админами
    users = User.objects.filter(is_moderator=False, is_superuser=False)
    return render(request, 'user/moderator.html', {'users': users})


def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user.is_moderator or user.is_superuser:
        return redirect(f'/user/{user_id}/?error=access_denied')

    return render(request, 'user/user_profile.html', {'user': user})
