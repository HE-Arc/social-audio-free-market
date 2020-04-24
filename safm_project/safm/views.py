import os
import mimetypes
from django.conf import settings
from rest_framework import filters, generics
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound

from .models import Sample
from .serializers import SampleSerializer

# Create your views here.

class QuickSearch(generics.ListAPIView):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'duration', 'tone', 'mode', 'tags__name']

class DownloadSample(APIView):
    
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
        