import environ
import os
import json
import requests
from openai import OpenAI
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.student_work.models import StudentWork
from apps.student_work.serializers import StudentWorkSerializer


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


class DecodeImageView(APIView):

    def post(self, request, *args, **kwargs):
        student_work_id = request.data.get("id")

        if not student_work_id:
            return Response({
                "error": "No student work ID provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            student_work = StudentWork.objects.get(pk=student_work_id)
        except StudentWork.DoesNotExist:
            return Response({
                "error": "Student work not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        image_data = student_work.image_work

        if not image_data:
            return Response({
                "error": "No image data found for the student work."},
                status=status.HTTP_400_BAD_REQUEST
            )

        BASE_DIR = '/home/diana/Desktop/Python/training/diplom/.env'
        env = environ.Env()
        environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
        mathpix_app_id = env("MATHPIX_APP_ID")
        mathpix_api_key = env("MATHPIX_API")
        my_path = "/home/diana/Desktop/Python/training/diplom/media/"

        # Call Mathpix API to decode the image
        response = requests.post(
            "https://api.mathpix.com/v3/text",
            files={"file": open(my_path + str(image_data), "rb")},
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

        if response.status_code != 200:
            return Response({
                "error": "Failed to decode image using Mathpix API."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Extract text from the response
        response_data = response.json()
        decoded_text = response_data.get("text")

        # Update text_work field in StudentWork model
        student_work.text_work = decoded_text
        student_work.save()

        return Response({
            "success": "Image decoded and text saved successfully."},
            status=status.HTTP_200_OK
        )


class ResponseTextView(APIView):

    def post(self, request, *args, **kwargs):
        student_work_id = request.data.get("id")

        if not student_work_id:
            return Response({
                "error": "No student work ID provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            student_work = StudentWork.objects.get(pk=student_work_id)
        except StudentWork.DoesNotExist:
            return Response({
                "error": "Student work not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        text_data = student_work.text_work
        if not text_data:
            return Response({
                "error": "No text data found for the student work."},
                status=status.HTTP_400_BAD_REQUEST
            )

        BASE_DIR = '/home/diana/Desktop/Python/training/diplom/.env'
        env = environ.Env()
        environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
        chatgpt_api_key = env("OPEN_AI_API")
        chatgpt_organization = env('OPEN_AI_ORGANIZATION')

        client = OpenAI(
            api_key=chatgpt_api_key,
            organization=chatgpt_organization
        )
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": """Ты учитель математики и проверяешь работу. 
            Проверь правильно ли решена эта работа, если нет то обьясни почему:""" + str(text_data)}]
        )

        # if chat_completion.status_code != 200:
        #     return Response({
        #         "error": "Failed to get completion from OpenAI API."},
        #         status=status.HTTP_500_INTERNAL_SERVER_ERROR
        #     )

        # Extract text from the response
        chatgpt_response = chat_completion.json()
        data = json.loads(chatgpt_response)
        completion_text = data['choices'][0]['message']['content']

        # Update proven_work field in StudentWork model
        student_work.proven_work = completion_text
        student_work.save()

        return Response({
            "success": "Text completed and saved successfully."},
            status=status.HTTP_200_OK
        )
