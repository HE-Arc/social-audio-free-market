from rest_framework import generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from safm_api.models import Sample
from safm_api.serializers import SampleSerializer


class SampleAdvancedSearchView(generics.ListAPIView):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
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
