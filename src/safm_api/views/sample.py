from django.http import HttpResponse, JsonResponse
from rest_framework import generics, status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from safm_api.models import Sample
from safm_api.serializers import SampleSerializer


class SampleView(generics.RetrieveAPIView, CreateModelMixin,
                 UpdateModelMixin, DestroyModelMixin):
    model = Sample
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        '''
        Overridden create method in order to assign the authenticated
        user and to return the newly created sample ID.
        '''
        serializer = SampleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Assign the authenticated user to the sample
        sample = serializer.save(user=request.user)

        return JsonResponse({
            'id': sample.id
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        '''
        Overridden patch method in order to only allow the sample
        owner to update it.
        '''
        sample = self.get_object()

        # The sample must belong to the user
        if sample.user.id == request.user.id:
            serializer = SampleSerializer(sample, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return HttpResponse(status=status.HTTP_200_OK)

        # The sample does not belong to the authenticated user
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        '''
        Overridden destroy method in order to only allow the
        sample owner to delete it.
        '''
        sample = self.get_object()

        # Tha sample must belong to the user
        if sample.user.id == request.user.id:
            sample.delete()

            return HttpResponse(status.HTTP_200_OK)

        # The sample does not belong to the authenticated user
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
