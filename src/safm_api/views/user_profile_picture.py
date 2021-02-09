import os
import mimetypes
from django.conf import settings
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from safm_api.models import UserProfile


class UserProfilePictureView(APIView):

    def get(self, request, pk):
        try:
            user_profile = UserProfile.objects.get(user=pk)
            picture_file = user_profile.profile_picture

            # Return the profile picture as a file attachment
            path_picture = os.path.join(settings.MEDIA_ROOT, picture_file.name)

            with open(path_picture, 'rb') as f:
                mime_type = mimetypes.MimeTypes().guess_type(picture_file.name)
                response = HttpResponse(f, content_type=mime_type)
                filename = picture_file.name.split('/')[-1]
                response['Content-Disposition'] = f'attachement; filename="{filename}"'
                # To allow the client to read it
                response['Access-Control-Expose-Headers'] = 'Content-Disposition'

            return response

        except BaseException:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
