from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        '''
        Log out the authenticated user.
        '''
        request.user.auth_token.delete()
        return HttpResponse(status=status.HTTP_200_OK)
