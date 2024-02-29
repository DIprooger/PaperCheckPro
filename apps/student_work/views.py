import re

import environ
import os
import json
import requests
from django.shortcuts import redirect, render
from openai import OpenAI
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

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

BASE_DIR = "/home/diana/Desktop/Python/training/diplom/.env"
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


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


class CreateWorkView(CreateAPIView):
    serializer_class = StudentWorkSerializer

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


class CreateExampleView(CreateAPIView):
    serializer_class = ExampleSerializer

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
                return Response({'success': DATA_UPDATED})
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


class UpdateProvenTextWorkView(APIView):

    def get(self, request, work_id):
        try:
            work = StudentWork.objects.get(pk=work_id)
            return render(
                request,
                'student_work/update_proven.html',
                {'proven_work': work.proven_work, 'work_id': work_id, 'work': work},
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
            if proven_work is not None:
                work.text_work = proven_work
                work.save()
                return Response({'success': DATA_UPDATED})
            else:
                return Response({
                    'error': NO_NEW_TEXT_PROVIDED},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except StudentWork.DoesNotExist:
            return Response({
                'error': STUDENT_WORK_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )


class UpdateExampleView(APIView):

    def get(self, request, example_id):
        try:
            example = Example.objects.get(pk=example_id)
            return Response({'text_work': example.text_work})
        except Example.DoesNotExist:
            return Response({
                'error': STUDENT_WORK_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request, example_id):
        try:
            example = Example.objects.get(pk=example_id)
            text_work = request.data.get('text_work')
            if text_work is not None:
                example.text_work = text_work
                example.save()
                return Response({'success': DATA_UPDATED})
            else:
                return Response({
                    'error': NO_NEW_TEXT_PROVIDED},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Example.DoesNotExist:
            return Response({
                'error': STUDENT_WORK_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )


class DecodeImageView(APIView):
    def get_id(self, request, work_id):
        id = request.data.get("work_id")

        if not id:
            return Response({
                "error": NO_STUDENT_WORK_ID_PROVIDED},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            student_work = StudentWork.objects.get(pk=id)
        except StudentWork.DoesNotExist:
            return Response({
                "error": STUDENT_WORK_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )
        return student_work

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

    def post(self, request, *args, **kwargs):

        student_work = self.get_id(request, id)
        image_data = student_work.image_work

        if not image_data:
            return Response({
                "error": NO_IMAGE_DATA_FOUND},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = self.mathpix(image_data)

        if response.status_code != 200:
            return Response({
                "error": FAILED_TO_DECODE_IMAGE},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Extract text from the response
        response_data = response.json()
        decoded_text = response_data.get("text")

        # Update text_work field in StudentWork model
        student_work.text_work = decoded_text
        student_work.save()

        return Response({
            "success": IMAGE_DECODED_AND_TEXT_SAVED},
            status=status.HTTP_200_OK
        )


class DecodeImageExapleView(DecodeImageView):
    def get_id(self, request, id):
        id = request.data.get("id")

        if not id:
            return Response({
                "error": NO_STUDENT_WORK_ID_PROVIDED},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            example = Example.objects.get(pk=id)
        except Example.DoesNotExist:
            return Response({
                "error": FOTO_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )
        return example


class ResponseTextView(APIView):

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

    def post(self, request, *args, **kwargs):

        decoder = DecodeImageView()
        decoder.post(request, *args, **kwargs)

        student_work_id = request.data.get("work_id")

        if not student_work_id:
            return Response({
                "error": NO_STUDENT_WORK_ID_PROVIDED},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            student_work = StudentWork.objects.get(pk=student_work_id)
        except StudentWork.DoesNotExist:
            return Response({
                "error": STUDENT_WORK_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )

        text_data = student_work.text_work

        if not text_data:
            return Response({
                "error": NO_TEXT_DATA_FOUND},
                status=status.HTTP_400_BAD_REQUEST
            )

        chat_completion = self.open_ai(
            text_data,
            request.data.get("example_id"),
            student_work.number_of_tasks
        )

        # Extract text from the response
        chatgpt_response = chat_completion.json()
        data = json.loads(chatgpt_response)
        completion_text = data["choices"][0]["message"]["content"]
        assessment = re.search(r"Оценка: (\d+)", completion_text)
        assessment = str(assessment.group(1))[:1]

        # Update proven_work field in StudentWork model
        student_work.proven_work = completion_text
        student_work.assessment = assessment
        student_work.save()

        return Response({
            "success": TEXT_COMPLETED_AND_SAVED},
            status=status.HTTP_200_OK
        )
