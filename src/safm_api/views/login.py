from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from safm_api.serializers import LoginSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        '''
        Try to authenticate the user based on the
        received credentials.
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = Token.objects.get_or_create(user=user)[0].key

        return JsonResponse({
            'userid': user.id,
            'username': user.username,
            'token': token,
        }, status=status.HTTP_200_OK)
