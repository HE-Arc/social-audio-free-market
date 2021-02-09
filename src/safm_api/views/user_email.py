from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from safm_api.models import UserProfile


class UserEmailView(APIView):

    def get(self, request, pk):
        user_profile = UserProfile.objects.get(user=pk)

        # Email is public or the profile belongs to the current user
        if user_profile and (
                user_profile.email_public or request.user.id == user_profile.id):
            user = User.objects.get(pk=pk)
            user_email = user.email

            return JsonResponse({
                'email': user_email
            }, status=status.HTTP_200_OK)

        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
