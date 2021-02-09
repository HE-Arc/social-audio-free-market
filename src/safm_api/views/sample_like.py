from django.http import HttpResponse, JsonResponse
from rest_framework import generics, status
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from safm_api.models import Sample, SampleLike


class SampleLikeView(generics.RetrieveAPIView, CreateModelMixin, DestroyModelMixin):
    model = Sample
    queryset = Sample.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        Overridden get method in order to return whether the
        given sample belongs to the authenticated user samples
        likes or not.
        '''
        sample = self.get_object()

        # The sample is liked by the user
        if SampleLike.objects.filter(sample=sample).filter(user=request.user).exists():
            return JsonResponse({
                'liked': True
            }, status=status.HTTP_200_OK)

        # The sample is not liked by the user
        return JsonResponse({
            'liked': False
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        Overridden post method in order to add the given sample
        to the authenticated user samples likes.
        '''
        sample = self.get_object()

        SampleLike.objects.get_or_create(
            user=request.user,
            sample=sample,
        )

        return HttpResponse(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        '''
        Overridden delete method in order to remove the given sample
        from the authenticated user samples likes.
        '''
        sample = self.get_object()

        sample_like = SampleLike.objects.filter(sample=sample).filter(user=request.user)
        sample_like.delete()

        return HttpResponse(status=status.HTTP_200_OK)
