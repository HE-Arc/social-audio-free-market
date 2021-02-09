from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from safm_api.serializers import UserSerializer


class RegisterView(generics.CreateAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        '''
        Overridden create method in order to return the authentication token
        after a successful registration.
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get_or_create(user=user)[0].key

        return JsonResponse({
            'userid': user.id,
            'username': user.username,
            'token': token,
        }, status=status.HTTP_201_CREATED)
