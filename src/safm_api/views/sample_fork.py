from rest_framework import generics
from safm_api.models import Sample
from safm_api.serializers import SampleSerializer


class SampleForkFromView(generics.ListAPIView):
    serializer_class = SampleSerializer

    def get_queryset(self):
        return Sample.objects.filter(forks_to=self.kwargs['pk'])


class SampleForkToView(generics.ListAPIView):
    serializer_class = SampleSerializer

    def get_queryset(self):
        return Sample.objects.filter(forks=self.kwargs['pk'])
