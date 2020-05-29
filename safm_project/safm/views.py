import os
import mimetypes
from django.conf import settings
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from rest_framework import filters, generics
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.filters import OrderingFilter

from django.contrib.auth.models import User
from .models import *
from .serializers import *

# Create your views here.

class Logout(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return HttpResponse(status=status.HTTP_200_OK)


class QuickSearch(generics.ListAPIView):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'tempo', 'key', 'mode', 'duration', 'tags__name', 'user__username']


class AdvancedSearch(generics.ListAPIView):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'name': ['icontains'],
        'user__username': ['icontains'],
        'duration': ['gte', 'lte'],
        'tempo': ['gte', 'lte'],
        'key': ['exact'],
        'mode': ['exact'],
        'tags__name': ['icontains'],    # How to use AND condition ?
    }
    ordering_fields = [
        'name',
        'user__username',
        'duration',
        'tempo',
        'key',
    ]


class SamplePage(APIView):

    def get(self, request, sample_id):
        sample = Sample.objects.filter(id=sample_id).get()
        serializer = SampleSerializer(sample)

        return JsonResponse(serializer.data)


class SampleFile(APIView):
    
    def get(self, request, sample_id):
        file = Sample.objects.filter(id=sample_id).values('file').get()

        if file:
            path_to_file = os.path.join(settings.MEDIA_ROOT, file['file'])
            with open(path_to_file, 'rb') as sample_file:
                mime_type = mimetypes.MimeTypes().guess_type(file['file'][0])
                response = HttpResponse(sample_file, content_type=mime_type)
                filename = file['file'].split('/')[-1]
                response['Content-Disposition'] = f'attachement; filename="{filename}"'

            return response
        else:
            return HttpResponseNotFound('No matching file found.')
        

class UserProfilePage(APIView):

    def get(self, request, username):

        # Can do better ?

        user = User.objects.filter(username=username).values('id')
        if user.exists():
            user_id = user[0]['id']
            user_profile = UserProfile.objects.filter(user_id=user_id)
            if user_profile.exists():
                user_profile_serializer = UserProfileSerializer(user_profile[0])

                return JsonResponse(user_profile_serializer.data)

        return HttpResponseNotFound('No matching user profile found.')
              

class UserSamples(APIView):

    def get(self, request, username):

        # Can do better ?

        user = User.objects.filter(username=username).values('id')
        if user.exists():
            user_id = user[0]['id']
            user_samples = Sample.objects.filter(user_id=user_id)
            sample_serializer = SampleSerializer(user_samples, many=True)

            return JsonResponse(sample_serializer.data, safe=False)

        return HttpResponseNotFound('No matching user found.')
        