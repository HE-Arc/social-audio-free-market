from rest_framework import filters, generics

from .models import Sample
from .serializers import SampleSerializer

# Create your views here.

class QuickSearch(generics.ListAPIView):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'duration', 'tone', 'mode', 'tags__name']
