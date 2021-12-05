from django.urls import path
from . import views


urlpatterns = [
   # balanceGame 밸런스게임 조회
   path('',views.balanceGame),
   # 게임투표
   path('vote/',views.game_vote),
   # vote_update 투표결과 반환(현재 질문 유지)
   path('vote_update/<int:pk>/',views.vote_update),

]

 