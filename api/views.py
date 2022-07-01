
# Create your views here.
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Challenge, GroupPurchase
from api.serializers import ChallengeSerializer, GroupPurchaseSerializer


# 함께해요 챌린지 로그인 구현후 회원 퍼미션 추가하기
class ChallengeView(APIView):
    def get(self, request):
        challenges = Challenge.objects.all().order_by('-created_at')
        serializer = ChallengeSerializer(challenges, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)


    def post(self, request):
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
        serializer = ChallengeSerializer(challenge, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


# 같이 사요 공동구매
class PurchaseView(APIView):
    def get(self, request):
        purchases = GroupPurchase.objects.all().order_by('-created_at')
        serializer = GroupPurchaseSerializer(purchases, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)


    def post(self, request):
        serializer = GroupPurchaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class PurchaseDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(GroupPurchase, pk=pk)

    def get(self, request, pk):
        purchase = self.get_object(pk)
        serializer = GroupPurchaseSerializer(purchase)
        return JsonResponse(serializer.data, status=201)

    def patch(self, request, pk):
        purchase = self.get_object(pk)
        serializer = GroupPurchaseSerializer(purchase, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)