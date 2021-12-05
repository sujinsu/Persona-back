
from rest_framework import status
from .serializers import UserSerializer

from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user_model


from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import User


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get('username')
    try:
        user = get_user_model().objects.get(username=username)
        return Response({'err':'이미 등록된 username입니다.'})
    except:
        data = request.data
        user = User.objects.create(first_name=data['first_name'], last_name=data['last_name'], 
        password=data['password'], username=data['username'], email=data['email'], nickname=data['nickname'])
        user.set_password(request.data.get('password'))
        user.save()
        return Response({'msg':'success'}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT','POST','DELETE'])
def profile(request):
    user = User.objects.filter(id=request.user.id)
    # 요청자 정보 조회
    if request.method =='GET':
        
        serializer = UserSerializer(user,many=True)
        return Response(serializer.data)

    # 요청자 자기소개 수정
    elif request.method == 'PUT':
    
        # user.profile_content = request.data['profile_content']
        user.update(profile_content=request.data['profile_content'])
        serializer = UserSerializer(user,many=True)
        return Response(serializer.data)
    

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 해당 유저 탈퇴
    elif request.method == 'DELETE':
        user = User.objects.filter(id=request.user.id)
        user.delete()
        return Response({ 'id': request.user.id}, status=status.HTTP_204_NO_CONTENT)


# 유저이름 변경
@api_view(['PUT'])
def profile_username_upload(request):
    if request.method == 'PUT':
        user = User.objects.filter(id=request.user.id)
        user.update(nickname=request.data['nickname'])
        serializer = UserSerializer(user,many=True)
        print(request.data['nickname'])
        return Response(serializer.data)
    
# 유저 이미지 변경
@api_view(['PUT'])
def profile_image_upload(request):
    if request.method == 'PUT':
        user = User.objects.filter(id=request.user.id)
        user.update(image=request.data['image'])
        serializer = UserSerializer(user,many=True)
        print(request.data['image'])
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def is_superuser(request):
    username = request.data.get('username')
    user = get_object_or_404(get_user_model(), username=username)
    return Response(user.is_superuser)


