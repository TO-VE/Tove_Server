
# Create your views here.
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Challenge
from api.serializers import ChallengeSerializer


class UserIsAnonymous(Exception):
    pass


def user_authenticate(request):
    if request.user.is_anonymous:
        raise UserIsAnonymous

class HelloView(APIView):
    def get(self, request):
        return Response("GET Hello", status=200)

    def post(self, request):
        return Response("POST Hello", status=200)

    def patch(self, request):
        return Response("PATCH Hello", status=200)

    def delete(self, request):
        return Response("DELETE Hello", status=200)


class ChallengeView(APIView):
    def get(self, request):
        user_authenticate(request)
        challenges = Challenge.objects.all().order_by('-created_at')
        serializer = ChallengeSerializer(challenges, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)


    def post(self, request):
        user_authenticate(request)
        serializer = ChallengeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class ChallengeDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(Challenge, pk=pk)

    def get(self, request, pk):
        challenge = self.get_object(pk)
        serializer = ChallengeSerializer(challenge)
        return JsonResponse(serializer.data, status=201)

    def patch(self, request, pk):
        challenge = self.get_object(pk)
        serializer = ChallengeSerializer(challenge, data=request.data, partial=True) # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)