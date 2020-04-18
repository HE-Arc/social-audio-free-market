from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Sample
from .serializers import SampleSerializer

# Create your views here.

@csrf_exempt
def samples(request):
    if request.method == 'GET':
        samples = Sample.objects.all()
        s = SampleSerializer(samples, many=True)
        return JsonResponse(s.data, safe=False)
