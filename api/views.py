# Create your views here.
import datetime
from datetime import timedelta

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.models import Challenge, GroupPurchase, Vegan, CO2Cal
from api.serializers import ChallengeSerializer, GroupPurchaseSerializer, VeganSerializer, SignUpSerializer, \
    UserSerializer, CO2CalSerializer

class TestView(APIView):
    def get(self, request):
        return Response("GET Hello", status=200)


# 회원가입
class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # jwt token 접근해주기
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            return Response(
                {
                    "user": serializer.data,
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=200,
            )
            # res.set_cookie("access", access_token, httponly=True)
            # res.set_cookie("refresh", refresh_token, httponly=True)
        return Response(serializer.errors, status=400)


class SigninView(APIView):

    def post(self, request):
        user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )
        if user is not None:
            serializer = UserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            return Response(
                {
                    "user": serializer.data,
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=200,
            )
        else:
            return Response(status=200)


# 함께해요 챌린지 로그인 구현후 회원 퍼미션 추가하기
class ChallengeView(APIView):

    def get(self, request):
        challenges = Challenge.objects.all().order_by('-created_at')
        serializer = ChallengeSerializer(challenges, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)

    def post(self, request):
        data = request.data
        data['author'] = request.user.id
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
        if challenge.author == request.user:
            serializer = ChallengeSerializer(challenge, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201, safe=False)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse({"유저 불일치!"}, status=400)


# 같이 사요 공동구매
class PurchaseView(APIView):

    def get(self, request):
        purchases = GroupPurchase.objects.all().order_by('-created_at')
        serializer = GroupPurchaseSerializer(purchases, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)

    def post(self, request):
        data = request.data
        data['author'] = request.user.id
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
        if purchase.author == request.user:
            serializer = GroupPurchaseSerializer(purchase, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse({"유저 불일치!"}, status=400)


# 비건 단계
class VeganCalView(APIView):

    def get(self, request):
        user = request.user
        end_date = datetime.datetime.now()
        start_date = end_date - timedelta(days=7)
        veglevels = Vegan.objects.filter(user=user, created_at__range=(start_date, end_date))
        veganserializer = VeganSerializer(veglevels, many=True)

        co2level = CO2Cal.objects.get(user=user)
        co2calserializer = CO2CalSerializer(co2level)
        return JsonResponse({
            "veganlevel": veganserializer.data,
            "co2level": co2calserializer.data
        }, status=200, safe=False)

    def post(self, request):
        user = request.user
        foods = request.data.get('foods', None)
        if "돼지고기" not in foods or "소고기" not in foods:
            level = "Flexitarian"
        elif "닭고기" not in foods:
            level = "Pollo"
        elif "생선" not in foods:
            level = "Pesco"
        elif "달걀" not in foods and "우유" not in foods:
            level = "Lacto Ovo"
        elif "달걀" not in foods and "우유" in foods:
            level = "Ovo"
        elif "달걀" in foods and "우유" not in foods:
            level = "Lacto"
        else:
            level = "Vegan"
        veglevel = Vegan.objects.create(user=user, level=level)
        veganserializer = VeganSerializer(veglevel)

        lev = foodtoCO2(foods)
        print(lev)
        co2level, check = CO2Cal.objects.update_or_create(user=request.user, level=lev)
        print(co2level)
        co2calserializer = CO2CalSerializer(co2level)
        return JsonResponse(
            {
                "veganlevel": veganserializer.data,
                "co2level": co2calserializer.data
            }, status=200, safe=False)


def foodtoCO2(foods):
    score = 0
    for i in foods:
        if "닭고기" in i:
            score += 753
        elif "소고기" in i:
            score += 2816
        elif "돼지고기" in i:
            score += 563
        elif "생선" in i:
            score += 300
        elif "달걀" in i:
            score += 225
        else:
            score += 600

    if score == 0:
        level = 0
    elif 0 < score <= 1315:
        level = 1
    elif 1315 < score <= 2688:
        level = 2
    elif 2688 < score <= 3943:
        level = 3
    elif 3943 < score <= 5257:
        level = 4
    else:
        level = 5
    return level
