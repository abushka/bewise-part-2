from django.shortcuts import render
from django.http import HttpResponse
from .models import CustomUser, AudioRecord
from django.conf import settings
import os

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, AudioSerializer

from pydub import AudioSegment
from pydub.exceptions import PydubException

@api_view(['POST'])
def create_user(request):
    username = request.data.get('username')
    if not username:
        raise ValueError("Invalid username")

    try:
        user = CustomUser.objects.get(username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        user = CustomUser(username=username)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)


@api_view(['POST'])
def add_audio(request):
    user_id = request.data.get('user_id')
    access_token = request.data.get('access_token')
    file = request.FILES.get('audio')

    user = CustomUser.objects.filter(id=user_id, access_token=access_token).first()

    if user is None:
        return Response({'error': 'Invalid user_id or access_token'}, status=400)

    # Проверка формата файла
    if not file.name.endswith('.wav'):
        return Response({'error': 'Invalid file format. Only WAV files are allowed.'}, status=400)

    try:
        # Конвертация файла в формат MP3
        audio = AudioSegment.from_file(file, format='wav')
        mp3_file = file.name.replace('.wav', '.mp3')
        audio.export(mp3_file, format='mp3')

        # Сохранение записи аудиофайла
        audio_record = AudioRecord(user=user, file=mp3_file)
        audio_record.save()

        serializer = AudioSerializer(audio_record)

        # Generate the URL for the audio file
        url = request.build_absolute_uri(f'/record?id={audio_record.id}&user={user_id}')

        # Append the URL to the serializer data
        serializer_data = serializer.data
        serializer_data['url'] = url

        return Response(serializer_data)

    except PydubException:
        return Response({'error': 'Failed to process audio file.'}, status=500)


def record_view(request):
    record_id = request.GET.get('id')
    user_id = request.GET.get('user')

    # Retrieve the audio record based on the provided IDs
    audio = AudioRecord.objects.filter(id=record_id, user__id=user_id).first()

    if audio is None:
        return HttpResponse('Audio not found', status=404)

    # Build the file path
    file_path = os.path.join(settings.MEDIA_ROOT, str(audio.file))

    # Check if the file exists
    if not os.path.exists(file_path):
        return HttpResponse('Audio file not found', status=404)

    # Open the file and read its content
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='audio/mp3')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(audio.file.name)
        return response