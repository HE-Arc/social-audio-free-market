from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from safm_api.models import Sample
from safm_api.serializers import SampleSerializer


class UserSamplesView(generics.ListAPIView):
    serializer_class = SampleSerializer

    def get_queryset(self):
        return Sample.objects.filter(user=self.kwargs['pk'])


class UserSamplesCountView(APIView):

    def get(self, request, pk):
        count = len(Sample.objects.filter(user=self.kwargs['pk']))
        return JsonResponse({
            'count': count
        }, status=status.HTTP_200_OK)
