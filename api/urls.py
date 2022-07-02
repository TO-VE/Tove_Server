from django.urls import path

from api.views import *

urlpatterns = [
    path("signup/", SignUpView.as_view()), #회원가입하기
    path('challenge', ChallengeView.as_view()),
    path('challenge/<int:pk>', ChallengeDetail.as_view()),
    path('purchase', ChallengeView.as_view()),
    path('purchase/<int:pk>', ChallengeDetail.as_view()),
    path('vegan', VeganView.as_view()),
]