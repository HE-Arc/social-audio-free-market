import os
from django.conf import settings
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.mixins import UpdateModelMixin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from safm_api.models import UserProfile
from safm_api.serializers import UserProfileSerializer


class UserProfileView(generics.RetrieveAPIView, UpdateModelMixin):
    model = UserProfile
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        '''
        Overridden update method in order to only allow the profile
        owner to update it and to remove the old profile picture
        when a new one is uploaded.
        '''
        profile = self.get_object()

        # The profile must belong to the user
        if profile.user == request.user:
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            # Remove the old profile picture when a new one is uploaded
            if request.data.get('profile_picture') and not profile.has_default_picture:
                path_old_picture = os.path.join(settings.MEDIA_ROOT,
                                                profile.profile_picture.name)
                os.remove(path_old_picture)

            serializer.save()

        # The profile does not belong to the authenticated user
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
