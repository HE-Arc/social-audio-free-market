import os
import re
import mimetypes
import wave
from django.conf import settings
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from rest_framework import filters, generics
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.filters import OrderingFilter

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import *
from .serializers import *

# Create your views here.

class Logout(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return HttpResponse(status=status.HTTP_200_OK)


class Register(generics.CreateAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        '''
        Overriden create method in order to return the authentication token
        after a successful registration.
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Checks password confirmation
        if request.POST.get('password') != request.POST.get('password_confirm'):
            return JsonResponse({'password_confirm': 'Password confirmation does not match.'}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        token = Token.objects.get_or_create(user=serializer.instance)[0] # Returns tuple

        return JsonResponse({'token': token.key}, status=status.HTTP_201_CREATED)


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
    
    #TODO: other APIView class ?
    
    def get(self, request, sample_id):
        sample = Sample.objects.filter(id=sample_id).get()
        serializer = SampleSerializer(sample)

        return JsonResponse(serializer.data)


class SampleUpload(generics.CreateAPIView):
    model = Sample
    serializer_class = SampleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        '''
        Overriden create method in order to set the current user
        to the uploaded sample.
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)        
        sample = self.perform_create(serializer)

        if sample:
            # Sample key
            key = request.POST.get('key')
            if key in [item.value for item in Sample.Key]:
                sample.key = key

            # Sample mode
            mode = request.POST.get('mode')
            if mode in [item.value for item in Sample.Mode]:
                sample.mode = mode

            # Adds the sample tags
            tags = re.escape(request.POST.get('tags', ''))
            tags_list = [tag.strip() for tag in tags.split(',')]
            for tag_name in tags_list:
                tag = Tag.objects.get_or_create(name=tag_name)[0] # Returns a tuple
                sample.tags.add(tag)

            # Automatically deducted sample properties
            sample.deduce_properties()

            sample.save()
        
            return JsonResponse({'id': sample.id}, status=status.HTTP_201_CREATED)

        return JsonResponse({'error': 'You are not logged in.'}, status=status.HTTP_401_UNAUTHORIZED)

    def perform_create(self, serializer):
        '''
        Overriden perform_create method in order to set the current
        user to the SampleSerializer before save.
        '''
        user = self.request.user
        if user:
            return serializer.save(user=user)
        
        return False


class SampleFile(APIView):
    
    def get(self, request, sample_id):
        sample = Sample.objects.get(pk=sample_id)
        sample_file = sample.file

        if sample:
            if request.auth:
                # If the user is authenticated, adds this sample to its downloads
                UserSampleDownload.objects.get_or_create(
                    user=request.user,
                    sample=sample
                )
                
            # Returns the audio file as a file attachment
            path_to_file = os.path.join(settings.MEDIA_ROOT, sample_file.name)
            with open(path_to_file, 'rb') as f:
                mime_type = mimetypes.MimeTypes().guess_type(sample_file.name)
                response = HttpResponse(f, content_type=mime_type)
                filename = sample_file.name.split('/')[-1]
                response['Content-Disposition'] = f'attachement; filename="{filename}"'
                response['Access-Control-Expose-Headers'] = 'Content-Disposition' # To allow the client to read it

            return response
        else:
            return HttpResponseNotFound('No matching file found.')
        

class UserProfilePage(APIView):

    def get(self, request, username):

        #TODO: Can do better ?

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

        #TODO: Can do better ?

        user = User.objects.filter(username=username).values('id')
        if user.exists():
            user_id = user[0]['id']
            user_samples = Sample.objects.filter(user_id=user_id)
            sample_serializer = SampleSerializer(user_samples, many=True)

            return JsonResponse(sample_serializer.data, safe=False)

        return HttpResponseNotFound('No matching user found.')
        