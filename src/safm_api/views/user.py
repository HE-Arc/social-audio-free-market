from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.mixins import UpdateModelMixin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from safm_api.serializers import UserSerializer


class UserView(generics.GenericAPIView, UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        '''
        Update the authenticated user based on the
        received data.
        '''
        if request.user.id == kwargs['pk']:
            return self.partial_update(request, *args, **kwargs)

        # The given user pk does not match with the authenticated user
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
