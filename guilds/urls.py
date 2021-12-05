from django.urls import path
from . import views


urlpatterns = [

    path('', views.guild_list_create),
    
    path('myguild/', views.my_guild),
    
    # 특정 길드 정보 수정 및 삭제
    path('<int:guild_pk>/', views.guild_update_delete),
    
    # 길드 생성시 태그도 저장
    # path('tag_create/',views.tag_create),

    # 현재 유저가 매니저인 길드 조회
    path('user_manager/', views.user_manager),


    # 현재 유저 매니저 여부 확인 
    path('<int:guild_pk>/is_manager/', views.is_manager),
    
    # 현재 유저 현재 길드 유저 확인 or 탈퇴
    path('<int:guild_pk>/is_member/', views.is_member),
    # 현재 유저 현재 길드 가입신청 확인 or 처리
    path('<int:guild_pk>/guild_signup/', views.guild_signup),

    # guild_signup_list 모드 조회
    path('guild_signup_list/', views.guild_signup_list),

    # signup_admit_delete 길드 가입 요청 수락 or 거절
    path('<int:guild_pk>/signup_admit_delete/<int:user_pk>/', views.signup_admit_delete),

    

    path('<int:guild_pk>/article/', views.article_list_create),
    # 해당 길드 해당 글 
    path('<int:guild_pk>/article/<int:article_pk>/', views.article_detail),
    # is_my_guildarticle 해당 글 해당 길드에서 해당 유저가 쓴글인가
    path('<int:guild_pk>/is_my_guildarticle/<int:article_pk>/', views.is_my_guildarticle),
   
    path('<int:guild_pk>/myarticle/',views.my_article),
     # user_article 현재 유저의 작성 글 전체 조회
    path('user_article/',views.user_article),
    # 좋아요 한 글인지 초기확인
    path('<int:guild_pk>/mylikearticle/',views.my_like_article),
    # 좋아요 동작 
    path('<int:guild_pk>/article/<int:article_pk>/like/', views.article_like),

    # guild_article_cnt 해당 길드 몇번째 글인지 조회
    path('<int:guild_pk>/guild_article_cnt/',views.guild_article_cnt),


    # 길드 해시태그로 검색
    path('search/<tag>/', views.search_guildtag),
    path('delete_tag/<tag_pk>/',views.delete_tag),

    # update_guildtag 해당 길드 태그 추가 or 조회
    path('<int:guild_pk>/guildtag_list_update/', views.guildtag_list_update),

    # 좋아요 알림을 위한 좋아요 동작 시 알림 조회, 생성, 삭제
    path('like_alram/<int:article_pk>/',views.like_alram),
    # like_alram_list 조회
    path('like_alram_list/',views.like_alram_list)

]