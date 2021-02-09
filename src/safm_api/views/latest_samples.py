from rest_framework import generics
from safm_api.models import Sample
from safm_api.serializers import SampleSerializer


class LatestSamplesView(generics.ListAPIView):
    serializer_class = SampleSerializer
    limit = 8  # Number of Samples to return

    def get_queryset(self):
        return Sample.objects.order_by('-datetime_upload')[:self.limit]
