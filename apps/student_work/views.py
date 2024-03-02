import re
import environ
import os
import json
import requests
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from openai import OpenAI
from rest_framework import status
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from apps.student_work.forms import ExampleForm, StudentWorkForm
from apps.student_work.models import (
    StudentWork,
    Example
)
from apps.student_work.serializers import (
    StudentWorkSerializer,
    ExampleSerializer
)

from apps.student_work.error_messages import (
    NO_STUDENT_WORK_ID_PROVIDED,
    NO_IMAGE_DATA_FOUND,
    FAILED_TO_DECODE_IMAGE,
    FOTO_NOT_FOUND,
    STUDENT_WORK_NOT_FOUND,
    NO_TEXT_DATA_FOUND,
    NO_RESPONSE_FROM_OPENAI, NO_NEW_TEXT_PROVIDED
)
from apps.student_work.success_messages import (
    IMAGE_DECODED_AND_TEXT_SAVED,
    TEXT_COMPLETED_AND_SAVED, DATA_UPDATED,
)
from apps.user.models import User

BASE_DIR = "/home/diana/Desktop/Python/training/diplom/.env"
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


@method_decorator(login_required, name='dispatch')
class AllStudentWorksView(APIView):
    serializer_class = StudentWorkSerializer

    def get(self, request: Request, *args, **kwargs):
        works = StudentWork.objects.all()

        if not works:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data=[]
            )

        serializer = self.serializer_class(works, many=True)

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )


# <<<<<<< HEAD
# @method_decorator(login_required, name='dispatch')
# class CreateWorkView(CreateAPIView):
#     serializer_class = StudentWorkSerializer
#
#     def post(self, request: Request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
# =======
# @method_decorator(login_required, name='dispatch')
# class CreateWorkView(View):
#     def get(self, request):
#         serializer = StudentWorkSerializer()
#         # Получение имени ученика
#         student_name = request.user.first_name  # Замените на реальное имя, полученное из данных запроса или сессии
#         context = {'form': serializer, 'student_name': student_name}
#         return render(request, 'student_work/create_work.html', context)
#
#     def post(self, request):
#         serializer = StudentWorkSerializer(data=request.POST, files=request.FILES)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             messages.success(request, 'Работа успешно сохранена.')
#             return redirect('user_profile')  # Замените 'user_profile' на имя вашего представления
#         return render(request, 'student_work/create_work.html', {'form': serializer})

class CreateStudentWorkView(View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        initial_data = {'teacher': request.user, 'student': user, 'writing_date': timezone.now()}
        form = StudentWorkForm(initial=initial_data)
        return render(request, 'student_work/create_work.html', {'form': form})

    def post(self, request, user_id):
        form = StudentWorkForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('user_profile', user_id=user_id)  # Redirect to success page after saving
        return render(request, 'student_work/create_work.html', {'form': form})


# @method_decorator(login_required, name='dispatch')
# class CreateExampleView(CreateAPIView):
#     serializer_class = ExampleSerializer
#
#     def post(self, request: Request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#
#             return Response(
#                 status=status.HTTP_201_CREATED,
#                 data=serializer.data
#             )
#         return Response(
#             status=status.HTTP_400_BAD_REQUEST,
#             data=serializer.errors
#         )


@method_decorator(login_required, name='dispatch')
class ExampleCreateView(View):
    def get(self, request):
        form = ExampleForm()
        return render(
            request,
            'student_work/example_create.html',
            {'form': form}
        )

    def post(self, request):
        form = ExampleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('moderator')
        return render(
            request,
            'student_work/example_create.html',
            {'form': form}
        )


@method_decorator(login_required, name='dispatch')
class UpdateTextWorkView(APIView):

    def get(self, request, work_id):
        try:
            work = StudentWork.objects.get(pk=work_id)
            return Response({'text_work': work.text_work})
        except StudentWork.DoesNotExist:
            return Response(
                {'error': STUDENT_WORK_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request, work_id):
        try:
            work = StudentWork.objects.get(pk=work_id)
            text_work = request.data.get('text_work')
            if text_work is not None:
                work.text_work = text_work
                work.save()
                return redirect('user_profile', user_id=work.student_id)
            else:
                return Response({
                    'success': False, 'error': NO_NEW_TEXT_PROVIDED},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except StudentWork.DoesNotExist:
            return Response({
                'error': STUDENT_WORK_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )


@method_decorator(login_required, name='dispatch')
class UpdateProvenTextWorkView(APIView):

    def get(self, request, work_id):
        try:
            work = StudentWork.objects.get(pk=work_id)
            user_id = work.student_id
            return render(
                request,
                'student_work/update_proven.html',
                {'proven_work': work.proven_work,
                 'assessment': work.assessment,
                 'work_id': work_id,
                 'work': work,
                 'user_id': user_id
                 },
            )  # Отображение страницы редактирования работы
        except StudentWork.DoesNotExist:
            return Response({
                'error': STUDENT_WORK_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request, work_id):
        try:
            work = StudentWork.objects.get(pk=work_id)
            proven_work = request.data.get('proven_work')
            assessment = request.data.get('assessment')
            if proven_work != work.proven_work or assessment != work.assessment:
                work.proven_work = proven_work
                work.assessment = assessment
                work.save()
                return Response({'message': 'Work updated successfully.'}, status=status.HTTP_200_OK)
            else:
                return redirect('update-work', work_id=work_id)  # Перенаправление на страницу редактирования
        except StudentWork.DoesNotExist:
            return Response({
                'error': STUDENT_WORK_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )


@method_decorator(login_required, name='dispatch')
class UpdateExampleView(APIView):

    def get(self, request, example_id):
        try:
            example = Example.objects.get(pk=example_id)
            # Передача текущего значения text_work в контекст шаблона
            old_text_work = example.text_work
            return render(request, 'student_work/update_example.html', {'example': example, 'old_text_work': old_text_work})
        except Example.DoesNotExist:
            raise Http404(STUDENT_WORK_NOT_FOUND)

    def post(self, request, example_id):
        try:
            example = Example.objects.get(pk=example_id)
            text_work = request.data.get('text_work')
            if text_work is not None:
                example.text_work = text_work
                example.save()
                return redirect('moderator')
            else:
                # Если text_work не передан, возвращаем ту же страницу с автозаполнением предыдущего текста
                old_text_work = example.text_work
                return render(request, 'student_work/update_example.html', {'example': example, 'old_text_work': old_text_work})
        except Example.DoesNotExist:
            raise Http404(STUDENT_WORK_NOT_FOUND)


@method_decorator(login_required, name='dispatch')
class ResponseTextView(APIView):
    def get_student_work(self, work_id):
        return get_object_or_404(StudentWork, pk=work_id)

    def mathpix(self, image_data):
        mathpix_app_id = env("MATHPIX_APP_ID")
        mathpix_api_key = env("MATHPIX_API")
        path_image = "/home/diana/Desktop/Python/training/diplom/media/"

        # Call Mathpix API to decode the image
        response = requests.post(
            "https://api.mathpix.com/v3/text",
            files={"file": open(path_image + str(image_data), "rb")},
            data={
                "options_json": json.dumps({
                    "math_inline_delimiters": ["$", "$"],
                    "rm_spaces": True
                }),
            },
            headers={
                "app_id": mathpix_app_id,
                "app_key": mathpix_api_key
            },
        )
        return response

    def open_ai(self, text_data, example_id, number_of_tasks):
        if not example_id:
            example_text = ""
        else:
            try:
                example = Example.objects.get(pk=example_id)
                example_text = example.text_work
            except Example.DoesNotExist:
                return Response({
                    "error": STUDENT_WORK_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND
                )

        chatgpt_api_key = env("OPEN_AI_API")
        chatgpt_organization = env('OPEN_AI_ORGANIZATION')

        if number_of_tasks == "5":
            patch_open_ai_text = \
                "/home/diana/Desktop/Python/training/diplom/apps/student_work/instruction_open_ai/five_shoolwork.txt"
        elif number_of_tasks == "10":
            patch_open_ai_text = \
                "/home/diana/Desktop/Python/training/diplom/apps/student_work/instruction_open_ai/ten_sholwoork.txt"
        else:
            patch_open_ai_text = \
                "/home/diana/Desktop/Python/training/diplom/apps/student_work/instruction_open_ai/other_instruction.txt"

        with open(patch_open_ai_text, 'r') as open_ai_text:
            open_ai_text = open_ai_text.read()
        content_system = open_ai_text + example_text

        client = OpenAI(
            api_key=chatgpt_api_key,
            organization=chatgpt_organization,
        )

        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": content_system},
                {"role": "user", "content": text_data}
            ]
        )
        if not chat_completion:
            return Response({
                "error": NO_RESPONSE_FROM_OPENAI},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return chat_completion

    def post(self, request, work_id, *args, **kwargs):
        student_work = self.get_student_work(work_id)
        image_data = student_work.image_work

        if not image_data:
            return Response({"error": NO_IMAGE_DATA_FOUND}, status=status.HTTP_400_BAD_REQUEST)

        response = self.mathpix(image_data)

        if response.status_code != 200:
            return Response({"error": FAILED_TO_DECODE_IMAGE}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_data = response.json()
        decoded_text = response_data.get("text")

        student_work.text_work = decoded_text
        student_work.save()

        text_data = decoded_text

        chat_completion = self.open_ai(
            text_data,
            request.data.get("example_id"),
            student_work.number_of_tasks
        )

        chatgpt_response = chat_completion.json()
        data = json.loads(chatgpt_response)
        completion_text = data["choices"][0]["message"]["content"]
        assessment = re.search(r"Оценка: (\d+)", completion_text)
        assessment = str(assessment.group(1))[:2]

        student_work.proven_work = completion_text
        student_work.assessment = assessment
        student_work.save()
        user_id = student_work.student_id
        return redirect(reverse('user_profile', kwargs={'user_id': user_id}))


class DecodeImageExapleView(APIView):
    def get_example_work(self, example_id):
        return get_object_or_404(Example, pk=example_id)

    def mathpix(self, image_data):
        mathpix_app_id = env("MATHPIX_APP_ID")
        mathpix_api_key = env("MATHPIX_API")
        path_image = "/home/diana/Desktop/Python/training/diplom/media/"

        # Call Mathpix API to decode the image
        response = requests.post(
            "https://api.mathpix.com/v3/text",
            files={"file": open(path_image + str(image_data), "rb")},
            data={
                "options_json": json.dumps({
                    "math_inline_delimiters": ["$", "$"],
                    "rm_spaces": True
                }),
            },
            headers={
                "app_id": mathpix_app_id,
                "app_key": mathpix_api_key
            },
        )
        return response

    def post(self, request, example_id, *args, **kwargs):
        example = self.get_example_work(example_id)
        image_data = example.image_work

        if not image_data:
            return Response({"error": NO_IMAGE_DATA_FOUND}, status=status.HTTP_400_BAD_REQUEST)

        response = self.mathpix(image_data)

        if response.status_code != 200:
            return Response({"error": FAILED_TO_DECODE_IMAGE}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_data = response.json()
        decoded_text = response_data.get("text")

        example.text_work = decoded_text
        example.save()

        user_id = request.user.id
        return redirect(reverse('moderator'))
