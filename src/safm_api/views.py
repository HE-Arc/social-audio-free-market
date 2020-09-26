import os, re, mimetypes
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
from django.dispatch import receiver
from django_rest_passwordreset.signals import *
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Tag, Sample, UserProfile, UserSampleDownload, SampleLike
from .serializers import UserSerializer, LoginSerializer, TagSerializer, SampleForkSerializer, SampleSerializer, UserDownloadSerializer, UserProfileSerializer, SampleLikeSerializer

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


@receiver(reset_password_token_created)
def send_password_reset_link(sender, instance, reset_password_token, *args, **kwargs):
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': '{0}/reset_password/{1}'.format(settings.CLIENT_APP_URL, reset_password_token.key),
        'token_expiration': settings.DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME,
    }
    
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # Title
        'SAFMarket - Password Reset',
        # Message
        email_plaintext_message,
        # From
        'noreply@safmarket.com',
        # To
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, 'text/html')
    msg.send()


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
            return Sample.objects.get(pk=kwargs['pk'])
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
        tags_str = re.escape(request.data.get('tags', '')).replace('\\', '') # re.escape can add backslashes in Python < 3.7
        tags_list = list(filter(self.regex_tags.match, [tag.strip() for tag in tags_str.split(',')]))
        
        for tag_name in tags_list:
            tag = Tag.objects.get_or_create(name=tag_name)[0] # Returns a tuple
            sample.tags.add(tag)

    def _set_forks_from_request(self, request, sample):
        '''
        Adds the Sample fork relations - based on the request - to the given Sample.
        '''
        forks_str = re.escape(request.data.get('forks_from', '')).replace('\\', '') # re.escape can add backslashes in Python < 3.7
        forks_list = list(filter(self.regex_forks.match, [fork.strip() for fork in forks_str.split(',')]))

        for fork_id in forks_list:
            fork = Sample.objects.get(pk=fork_id)
            sample.forks.add(fork)


class SampleFile(APIView):
    
    def get(self, request, pk, download):
        try:
            sample = Sample.objects.get(pk=pk)

            if download == 1:
                # Increments the sample number of downloads
                sample.number_downloads += 1
                sample.save()

                if request.auth:
                    # If the user is authenticated, adds this sample to its downloads
                    UserSampleDownload.objects.get_or_create(
                        user=request.user,
                        sample=sample
                    )
                
            # Returns the audio file as a file attachment
            path_to_file = os.path.join(settings.MEDIA_ROOT, sample.file.name)
            with open(path_to_file, 'rb') as f:
                mime_type = mimetypes.MimeTypes().guess_type(sample.file.name)
                response = HttpResponse(f, content_type=mime_type)
                ext = sample.file.name.split('.')[-1]
                filename = '{0}.{1}'.format(sample.name, ext)
                response['Content-Disposition'] = f'attachement; filename="{filename}"'
                response['Access-Control-Expose-Headers'] = 'Content-Disposition' # To allow the client to read it

            return response
        except:
            return HttpResponseNotFound('No matching file found.')


class ListLastUploadedSamples(generics.ListAPIView):
    serializer_class = SampleSerializer
    limit = 8 # Number of Samples to return

    def get_queryset(self):
        return Sample.objects.order_by('-datetime_upload')[:self.limit]


class ListSampleForkFrom(generics.ListAPIView):
    serializer_class = SampleSerializer

    def get_queryset(self):
        return Sample.objects.filter(forks_to=self.kwargs['pk'])
    

class ListSampleForkTo(generics.ListAPIView):
    serializer_class = SampleSerializer

    def get_queryset(self):
        return Sample.objects.filter(forks=self.kwargs['pk'])


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
            return UserProfile.objects.get(pk=kwargs['pk'])
        except:
            return None
              

class UserProfilePicture(APIView):

    def get(self, request, pk):
        user_profile = UserProfile.objects.get(user=pk)
        image_file = user_profile.profile_picture

        if image_file:
            path_to_file = os.path.join(settings.MEDIA_ROOT, image_file.name)
            with open(path_to_file, 'rb') as f:
                mime_type = mimetypes.MimeTypes().guess_type(image_file.name)
                response = HttpResponse(f, content_type=mime_type)
                filename = image_file.name.split('/')[-1]
                response['Content-Disposition'] = f'attachement; filename="{filename}"'
                response['Access-Control-Expose-Headers'] = 'Content-Disposition' # To allow the client to read it

            return response

        return HttpResponseNotFound('No matching file found.')


class UserSamples(generics.ListAPIView):
    serializer_class = SampleSerializer

    def get_queryset(self):
        return Sample.objects.filter(user=self.kwargs['pk'])
        

class UserSamplesCount(APIView):

    def get(self, request, pk):
        count = len(Sample.objects.filter(user=self.kwargs['pk']))
        return JsonResponse({'count': count}, status=status.HTTP_200_OK)


class UserEmail(APIView):

    def get(self, request, pk):
        user_profile = UserProfile.objects.get(user=pk)
        
        # Email is public or the profile belongs to the current user
        if user_profile and (user_profile.email_public or request.user.id == user_profile.id):
            user = User.objects.get(pk=pk)
            user_email = user.email

            return JsonResponse({'email': user_email}, status=status.HTTP_200_OK)

        return HttpResponseNotFound('No matching user found.')


class SampleLikeView(generics.GenericAPIView):
    unauthenticated = JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
    sample_not_found = JsonResponse({'detail': 'Sample not found.'}, status=status.HTTP_400_BAD_REQUEST)
    sample_like_not_found = JsonResponse({'detail': 'Sample like not found.'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        if self._is_authenticated(request):
            sample = self._sample_by_id(kwargs)

            if sample:
                sample_like = self._sample_like(sample, request.user)

                if sample_like.exists():
                    return JsonResponse({'liked': True}, status=status.HTTP_200_OK)

                return JsonResponse({'liked': False}, status=status.HTTP_200_OK)

            return self.sample_not_found

        return self.unauthenticated

    def post(self, request, *args, **kwargs):
        if self._is_authenticated(request):
            sample = self._sample_by_id(kwargs)

            if sample:
                SampleLike.objects.get_or_create(
                    user=request.user,
                    sample=sample
                )

                return JsonResponse({'detail': 'This sample is added to your likes.'}, status=status.HTTP_201_CREATED)

            return self.sample_not_found

        return self.unauthenticated

    def delete(self, request, *args, **kwargs):
        if self._is_authenticated(request):
            sample = self._sample_by_id(kwargs)

            if sample:
                sample_like = self._sample_like(sample, request.user)

                if sample_like:
                    sample_like.delete()

                    return JsonResponse({'detail': 'This sample is removed from your likes.'}, status=status.HTTP_200_OK)

                return self.sample_like_not_found

            return self.sample_not_found

        return self.unauthenticated

    def _is_authenticated(self, request):
        '''
        Returns wether the current user is authenticated or not.
        '''
        return request.user.is_authenticated

    def _sample_by_id(self, kwargs):
        '''
        Returns the Sample model associated to the pk parameter or None.
        '''
        try:
            return Sample.objects.get(pk=kwargs['pk'])
        except:
            return None

    def _sample_like(self, sample, user):
        '''
        Returns the SampleLike model associated to the given sample and user.
        '''
        return SampleLike.objects.filter(sample=sample).filter(user=user)


class UserSampleLikes(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_likes = SampleLike.objects.filter(user=user).order_by('-datetime_like')
        user_likes_serializer = SampleLikeSerializer(user_likes, many=True)

        return JsonResponse(user_likes_serializer.data, safe=False)
