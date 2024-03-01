from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

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
from rest_framework.response import Response
from rest_framework import status
from apps.student_work.models import StudentWork, Example


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('register'))


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


@method_decorator(login_required, name='dispatch')
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


# @method_decorator(login_required, name='dispatch')
# class UserDetailGenericView(RetrieveUpdateDestroyAPIView):
#     # permission_classes = [IsAuthenticated]
#     serializer_class = UserInfoSerializer
#
#     def get_object(self):
#         user_id = self.kwargs.get("user_id")
#
#         user_obj = get_object_or_404(User, id=user_id)
#
#         return user_obj
#
#     def get(self, request: Request, *args, **kwargs):
#         user = self.get_object()
#
#         serializer = self.serializer_class(user)
#
#         return Response(
#             status=status.HTTP_200_OK,
#             data=serializer.data
#         )
#
#     def put(self, request: Request, *args, **kwargs):
#         user = self.get_object()
#
#         serializer = self.serializer_class(
#             user,
#             data=request.data,
#             partial=True
#         )
#
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#
#             return Response(
#                 status=status.HTTP_200_OK,
#                 data=serializer.data
#             )
#         return Response(
#             status=status.HTTP_400_BAD_REQUEST,
#             data=serializer.errors
#         )
#
#     def delete(self, request: Request, *args, **kwargs):
#         user = self.get_object()
#
#         user.delete()
#
#         return Response(
#             status=status.HTTP_200_OK,
#             data=[]
#         )


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(
            request,
            'user/login.html',
            {'form': form}
        )

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_moderator:
                return redirect(reverse('moderator'))
            elif user.is_superuser:
                return redirect(reverse('admin_page'))
            else:
                return redirect(reverse('student_profile'))
        return render(
            request,
            'user/login.html',
            {'form': form}
        )


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(
            request,
            'user/register.html',
            {'form': form}
        )

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.is_moderator:
                return redirect('moderator')
            elif user.is_superuser:
                return redirect('admin_page')
            else:
                return redirect('student_profile')
        return render(
            request,
            'user/register.html',
            {'form': form}
        )


@method_decorator(login_required, name='dispatch')
class ModeratorView(View):
    def get(self, request):
        users = User.objects.filter(is_moderator=False, is_superuser=False)
        examples = Example.objects.all()
        return render(
            request,
            'user/moderator.html',
            {'users': users, 'examples': examples}
        )


@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if user.is_moderator or user.is_superuser:
            return redirect(f'/user/{user_id}/?error=access_denied')

        works = StudentWork.objects.filter(student=user)
        work_list = []

        for work in works:
            work_data = {
                'id': work.id,
                'name_work': work.name_work,
                'writing_date': work.writing_date,
                'assessment': work.assessment,

                # Добавьте другие поля работ, если нужно
            }
            work_list.append(work_data)

        return render(
            request,
            'user/user_profile.html',
            {'user': user, 'works': work_list, 'current_user': request.user}
        )


@method_decorator(login_required, name='dispatch')
class StudentProfileView(View):

    def get(self, request):
        return render(
            request,
            'user/student_profile.html',
            {'profile': request.user}
        )


@method_decorator(login_required, name='dispatch')
class GetUsersView(View):
    def get(self, request, *args, **kwargs):
        user_ids = request.GET.get('users', '').split(',')
        users = User.objects.filter(id__in=user_ids)
        user_list = [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name}
            for user in users]
        return JsonResponse(
            user_list,
            safe=False
        )


@method_decorator(login_required, name='dispatch')
class AdminPageView(View):
    model = User
    template_name = 'user/admin_page.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.filter(is_superuser=False)

    def get(self, request, *args, **kwargs):
        users = self.get_queryset()
        return render(
            request,
            self.template_name,
            {self.context_object_name: users})


@method_decorator([csrf_exempt, login_required], name='dispatch')
class DeleteUserView(View):
    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            # После удаления пользователя перенаправляемся на ту же страницу
            return redirect(reverse('admin_page'))
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Пользователь не найден.'})

    def get(self, request, user_id):
        return JsonResponse({'status': 'error', 'message': 'Неверный метод запроса.'})


@method_decorator(login_required, name='dispatch')
class WorkDeleteView(View):
    def post(self, request, work_id):
        work = get_object_or_404(StudentWork, id=work_id)
        user_id = work.student_id  # Получите идентификатор пользователя, связанного с работой
        work.delete()
        return redirect(reverse('user_profile', kwargs={'user_id': user_id}))

    def get(self, request, work_id):
        return redirect('user_profile')
