from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from . import views


urlpatterns = [
   path('signup/',views.signup),
   path('superuser/',views.is_superuser),
   path('api-token-auth/', obtain_jwt_token), 

   # get_profile 해당 유저 정보 조회 or 자기소개 수정
   path('profile/',views.profile),

   # profile_username_upload 해당 유저 이름 변경
   path('profile_username_upload/',views.profile_username_upload),

   # profile_image_upload 이미지 업로드 및 수정
   path('profile_image_upload/',views.profile_image_upload),

  
]
