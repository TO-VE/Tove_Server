from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import *

urlpatterns = [
    path('signup', SignUpView.as_view()), #회원가입하기
    path('signin', SigninView.as_view()), #로그인하기
    path('refresh', TokenRefreshView.as_view()),#토큰 재발급하기
    path('challenge', ChallengeView.as_view()),
    path('challenge/<int:pk>', ChallengeDetail.as_view()),
    path('purchase', PurchaseView.as_view()),
    path('purchase/<int:pk>', PurchaseDetail.as_view()),
    path('vegan', VeganCalView.as_view()),
    path('test', TestView.as_view()),
]