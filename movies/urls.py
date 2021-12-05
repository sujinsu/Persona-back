from django.urls import path, include
from . import views

app_name = 'movies' 
urlpatterns = [
    # 영화 추천 기능 
    path('recommendations/', views.movie_recommendation),
    # 요청온 영화 vue에서 검색해서 TMDB에서 json data받아서 
    # data에 실은 후에 요청 
    path('<int:val>/', views.movie_list_and_create),  # 권한: admin만
    # 등록된 영화 수정 & 삭제하기
    path('change/<int:api_id>/', views.movie_update_and_delete),
    # 등록 요청 온 영화를 보여주는 url & 등록 요청 폼을 생성하는 url
    path('request/', views.request_list_and_create),    # 권한: admin만
    # 영화 등록 폼 삭제하기 
    path('request/<int:form_pk>/', views.delForm),
    # 단일 영화 상세페이지
    path('detail/<int:api_id>/', views.movie_detail),
    # # 영화 좋아요한 유저 수 & 영화 좋아요하기
    path('<int:movie_pk>/like/', views.like_cnt_and_create), 
    # 해당 영화에 좋아요 눌렀는지 여부 확인
    path('<int:movie_pk>/isLiked/', views.isLiked),
    # 검색어로 DB내에서 찾기
    path('search/<str:keyword>/', views.searchKeyword),
    # review like/like누른 유저 수
    path('<int:review_pk>/review/like/', views.review_like_cnt_and_create),
    # 해당 리뷰에 좋아요 눌렀는지 여부 확인
    path('<int:review_pk>/review/isLiked/', views.isReviewLiked),
    # review 쓴 user 정보 가져오기
    path('<int:review_pk>/review/user/', views.get_review_user),
    # review list 가져오기 & review 생성하는 url
    path('<int:movie_pk>/review/', views.review_list_and_create),
    # api에서 불러온 영화가 DB에 있는 영환지 확인
    path('<int:api_id>/check/', views.isInDB),

    # 만들어진 모든 collection을 반환 & collection을 create
    path('collection/<int:val>/', views.collections_list_and_create),
    # pk로 collection 찾기
    # path('collection/get/<int:collection_pk>/', views.get_collection),
    # collection에 좋아요 눌렀는지 여부 확인
    path('<int:collection_pk>/collection/isLiked/', views.isCollectionLiked),
    # collection 좋아요한 유저 수 /collection like
    path('<int:collection_pk>/collection/like/', views.collection_like_cnt_and_create),
    # keyword로 collection title 검색
    path('search/collection/<str:keyword>/title/', views.search_collection_title),
    # keyword로 collection tag 검색
    path('search/collection/<str:keyword>/tag/', views.search_collection_tag),
    # 해당 컬렉션의 작성자와 로그인한 유저가 같은지 확인
    path('collection/user/<int:collection_pk>/', views.is_collection_user),
    # 해당 컬렉션 수정 및 삭제
    path('collection/change/<int:collection_pk>/', views.collection_update_and_delete),
    # 해당 컬렉션의 태그들 가져옴
    path('collection/<int:collection_pk>/tags/', views.get_collection_tags),

    # 프로필의 My likes에서 유저가 좋아요한 영화나 컬렉션 전체 들고오기
    path('get/mylikes/<int:val>/', views.get_my_likes),

]
