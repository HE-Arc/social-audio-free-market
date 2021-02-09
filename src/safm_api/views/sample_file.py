import os
import mimetypes
from django.conf import settings
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from safm_api.models import Sample, UserSampleDownload


class SampleFileView(APIView):

    def get(self, request, pk, download):
        try:
            sample = Sample.objects.get(pk=pk)

            if download == 1:
                # Increment the sample number of downloads
                sample.number_downloads += 1
                sample.save()

                if request.auth:
                    # Add the sample to the user downloads
                    UserSampleDownload.objects.get_or_create(
                        user=request.user,
                        sample=sample
                    )

            # Return the audio file as a file attachment
            path_to_file = os.path.join(settings.MEDIA_ROOT, sample.file.name)

            with open(path_to_file, 'rb') as f:
                mime_type = mimetypes.MimeTypes().guess_type(sample.file.name)
                response = HttpResponse(f, content_type=mime_type)
                ext = sample.file.name.split('.')[-1]
                filename = '{0}.{1}'.format(sample.name, ext)
                response['Content-Disposition'] = f'attachement; filename="{filename}"'
                # Allow the client to read it
                response['Access-Control-Expose-Headers'] = 'Content-Disposition'

            return response

        except BaseException:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
