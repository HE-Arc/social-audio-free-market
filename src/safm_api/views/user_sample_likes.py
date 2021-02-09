from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from safm_api.models import SampleLike
from safm_api.serializers import SampleLikeSerializer


class UserSampleLikesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_likes = SampleLike.objects.filter(
            user=user).order_by('-datetime_like')
        serializer = SampleLikeSerializer(user_likes, many=True)

        return JsonResponse(serializer.data, safe=False)
