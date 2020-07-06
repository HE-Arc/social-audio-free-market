import os
import re
import mimetypes
import wave
from django.conf import settings
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from rest_framework import filters, generics
from rest_framework.views import APIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.filters import OrderingFilter

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import *
from .serializers import *

from rest_framework.decorators import api_view, permission_classes

# Create your views here.

class Login(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = Token.objects.get_or_create(user=user)[0].key

        return JsonResponse({
            'token': token,
            'userid': user.id,
            'username': user.username
        }, status=status.HTTP_200_OK)


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
        user = serializer.save()
        token = Token.objects.get_or_create(user=user)[0].key

        return JsonResponse({
            'token': token,
            'userid': user.id,
            'username': user.username
        }, status=status.HTTP_201_CREATED)


class UserUpdate(generics.GenericAPIView, UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        if request.user.id == kwargs['pk']:
            return self.partial_update(request, *args, **kwargs)

        return JsonResponse({'detail': 'User does not belong to the user.'}, status=status.HTTP_401_UNAUTHORIZED)


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


class SampleView(generics.GenericAPIView):
    sample_not_found = JsonResponse({'detail': 'Sample not found.'}, status=status.HTTP_400_BAD_REQUEST)
    unauthenticated = JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
    sample_not_authorized = JsonResponse({'detail': 'Sample does not belong to the user.'}, status=status.HTTP_401_UNAUTHORIZED)
    regex_tags = re.compile(r'[a-z]+[a-z0-9]+')
    regex_forks = re.compile(r'\d')

    def get(self, request, *args, **kwargs):
        '''
        Retrieve Sample
        '''
        sample = self._sample_by_id(kwargs)
        if sample:
            serializer = SampleSerializer(sample)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
            
        return self.sample_not_found

    def post(self, request, *args, **kwargs):
        '''
        Create Sample
        '''
        if self._is_authenticated(request):
            serializer = SampleSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            sample = serializer.save(user=request.user)

            if sample:
                self._set_tags_from_request(request, sample)
                self._set_forks_from_request(request, sample)

                return JsonResponse({'id': sample.id}, status=status.HTTP_201_CREATED)

            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return self.unauthenticated

    def patch(self, request, *args, **kwargs):
        '''
        Update Sample
        '''
        if self._is_authenticated(request):
            sample = self._sample_by_id(kwargs)
            
            if sample:
                if self._sample_belongs_to_user(sample, request):
                    serializer = SampleSerializer(sample, data=request.data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    sample = serializer.save()

                    if sample:
                        sample.tags.clear()
                        self._set_tags_from_request(request, sample)

                        sample.forks.clear()
                        self._set_forks_from_request(request, sample)

                        return JsonResponse({'id': sample.id}, status=status.HTTP_200_OK)

                    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                return self.sample_not_authorized

            return self.sample_not_found

        return self.unauthenticated

    def delete(self, request, *args, **kwargs):
        '''
        Delete Sample
        '''
        if self._is_authenticated(request):
            sample = self._sample_by_id(kwargs)

            if sample:
                if self._sample_belongs_to_user(sample, request):
                    sample.delete()
                    return JsonResponse({'detail': 'Sample was successfully deleted.'}, status=status.HTTP_200_OK)
                
                return self.sample_not_authorized

            return self.sample_not_found

        return self.unauthenticated

    def _is_authenticated(self, request):
        '''
        Returns wether the current user is authenticated or not.
        '''
        return request.user.is_authenticated

    def _sample_by_id(self, kwargs):
        '''
        Returns the Sample model associated to the ID parameter or None.
        '''
        try:
            return Sample.objects.get(pk=kwargs['id'])
        except:
            return None

    def _sample_belongs_to_user(self, sample, request):
        '''
        Returns wether the given Sample belongs to the current user.
        '''
        return sample.user.id == request.user.id

    def _set_tags_from_request(self, request, sample):
        '''
        Adds the Tag relations - based on the request - to the given Sample.
        '''
        tags_str = re.escape(request.data.get('tags', ''))
        tags_list = list(filter(self.regex_tags.match, [tag.strip() for tag in tags_str.split(',')]))
        
        for tag_name in tags_list:
            tag = Tag.objects.get_or_create(name=tag_name)[0] # Returns a tuple
            sample.tags.add(tag)

    def _set_forks_from_request(self, request, sample):
        '''
        Adds the Sample fork relations - based on the request - to the given Sample.
        '''
        forks_str = re.escape(request.data.get('forks', ''))
        forks_list = list(filter(self.regex_forks.match, [fork.strip() for fork in forks_str.split(',')]))

        for fork_id in forks_list:
            fork = Sample.objects.get(pk=fork_id)
            sample.forks.add(fork)


class SampleFile(APIView):
    
    def get(self, request, sample_id, download):
        sample = Sample.objects.get(pk=sample_id)
        sample_file = sample.file

        if sample:
            if download == 1:
                if request.auth:
                    # If the user is authenticated, adds this sample to its downloads
                    UserSampleDownload.objects.get_or_create(
                        user=request.user,
                        sample=sample
                    )

                # Increments the sample number of downloads
                sample.number_downloads += 1
                sample.save()
                
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


class ListSampleForkFrom(generics.ListAPIView):
    serializer_class = SampleSerializer

    def get_queryset(self):
        # lookup_field only used in detail views
        return Sample.objects.filter(forks=self.kwargs['sample_id'])
    

class ListSampleForkTo(generics.ListAPIView):
    serializer_class = SampleSerializer

    def get_queryset(self):

        #FIXME

        # lookup_field only used in detail views
        return Sample.objects.filter(forks=self.kwargs['sample_id'])#.values('forks')


class UserDownloads(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_downloads = UserSampleDownload.objects.filter(user=user).order_by('-datetime_download')
        user_downloads_serializer = UserDownloadSerializer(user_downloads, many=True)

        return JsonResponse(user_downloads_serializer.data, safe=False)


class UserProfileView(generics.GenericAPIView):
    profile_not_found = JsonResponse({'detail': 'User profile not found.'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        '''
        Retrieve UserProfile
        '''
        profile = self._profile_by_id(kwargs)
        if profile:
            serializer = UserProfileSerializer(profile)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
            
        return self.profile_not_found

    def patch(self, request, *args, **kwargs):
        '''
        Update User Profile
        '''
        if request.user.is_authenticated:
            profile = self._profile_by_id(kwargs)

            if profile:
                if profile.user == request.user:
                    serializer = UserProfileSerializer(profile, data=request.data, partial=True)
                    serializer.is_valid(raise_exception=True)
    
                    # Removes the old profile picture if a new one is uploaded
                    if request.data.get('profile_picture'):
                        path_old_picture = os.path.join(settings.MEDIA_ROOT, profile.profile_picture.name)
                        os.remove(path_old_picture)

                    profile = serializer.save()

                    if profile:
                        return JsonResponse({'id': profile.id}, status=status.HTTP_200_OK)

                    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                return JsonResponse({'detail': 'Profile does not belong to the user.'}, status=status.HTTP_401_UNAUTHORIZED)

            return self.profile_not_found

        return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    def _profile_by_id(self, kwargs):
        '''
        Returns the UserProfile model associated to the ID parameter or None.
        '''
        try:
            return UserProfile.objects.get(pk=kwargs['id'])
        except:
            return None
              

class UserSamples(generics.ListAPIView):
    serializer_class = SampleSerializer

    def get_queryset(self):
        return Sample.objects.filter(user=self.kwargs['user_id'])
        

class UserSamplesCount(APIView):

    def get(self, request, user_id):
        count = len(Sample.objects.filter(user=self.kwargs['user_id']))
        return JsonResponse({'count': count}, status=status.HTTP_200_OK)


class UserProfilePicture(APIView):

    def get(self, request, user_id):
        user_profile = UserProfile.objects.get(user=user_id)
        image_file = user_profile.profile_picture

        if image_file:
            print(image_file)
            path_to_file = os.path.join(settings.MEDIA_ROOT, image_file.name)
            print(path_to_file)
            with open(path_to_file, 'rb') as f:
                mime_type = mimetypes.MimeTypes().guess_type(image_file.name)
                response = HttpResponse(f, content_type=mime_type)
                filename = image_file.name.split('/')[-1]
                response['Content-Disposition'] = f'attachement; filename="{filename}"'
                response['Access-Control-Expose-Headers'] = 'Content-Disposition' # To allow the client to read it

            return response

        return HttpResponseNotFound('No matching file found.')


class UserEmail(APIView):

    def get(self, request, user_id):
        user_profile = UserProfile.objects.get(user=user_id)
        
        if user_profile and user_profile.email_public:
            user = User.objects.get(pk=user_id)
            user_email = user.email

            return JsonResponse({'email': user_email}, status=status.HTTP_200_OK)

        return HttpResponseNotFound('No matching user found.')
