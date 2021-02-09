from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from safm_api.models import UserSampleDownload
from safm_api.serializers import UserDownloadSerializer


class UserDownloadsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_downloads = UserSampleDownload.objects.filter(
            user=user).order_by('-datetime_download')
        user_downloads_serializer = UserDownloadSerializer(
            user_downloads, many=True)

        return JsonResponse(user_downloads_serializer.data, safe=False)
