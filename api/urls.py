from django.urls import path

from api.views import *

urlpatterns = [
    path('challenge', ChallengeView.as_view()),
    path('challenge/<int:pk>', ChallengeDetail.as_view()),
    path('purchase', ChallengeView.as_view()),
    path('purchase/<int:pk>', ChallengeDetail.as_view()),
]