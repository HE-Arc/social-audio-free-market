from rest_framework import generics
from rest_framework.filters import SearchFilter
from safm_api.models import Sample
from safm_api.serializers import SampleSerializer


class SampleQuickSearchView(generics.ListAPIView):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    filter_backends = [SearchFilter]
    search_fields = [
        'name',
        'tempo',
        'key',
        'mode',
        'duration',
        'tags__name',
        'user__username'
    ]
