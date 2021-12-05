
from rest_framework.permissions import AllowAny

# Create your views here.

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from django.shortcuts import get_object_or_404,get_list_or_404,redirect
from django.views.decorators.http import require_POST
from django.http.response import JsonResponse
from django.contrib.auth import get_user_model

from .forms import GuildArticleForm
from .serializers import GuildSerializer,GuildArticleSerializer,GuildUserSerializer,GuildSignupSerializer,GuildTagSerializer,GuildArticleCountSerializer,AritcleLikeSerializer
from .models import Guild,GuildArticle,GuildSignup,GuildTag,GuildUser,GuildArticleCount,AritcleLike
# Create your views here.

@api_view(['GET', 'POST'])
def guild_list_create(request):
    if request.method == 'GET':
        guilds = Guild.objects.all().order_by('-pk')
        serializer = GuildSerializer(guilds, many=True)
        return Response(serializer.data)

    # 길드 생성
    elif request.method == 'POST':
        serializer = GuildSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            # 길드 매니저 == 요청 유저
            guildData = serializer.save(manager=request.user)       
            # 길드와 길드 유저 기록 : 첫 길드유저는 요청 유저
            guildUser = GuildUser(user=request.user,guild=guildData)
            guildUser.save()

            GuildTag.objects.create(tag=request.data['tag'],guild=guildData.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


    # 길드 생성
    elif request.method == 'POST':
        serializer = GuildSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            # 길드 매니저 == 요청 유저
            guildData = serializer.save(manager=request.user)       
            # 길드와 길드 유저 기록 : 첫 길드유저는 요청 유저
            guildUser = GuildUser(user=request.user,guild=guildData)
            guildUser.save()

            GuildTag.objects.create(tag=request.data['tag'],guild=guildData.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET','PUT', 'DELETE'])
# 특정 길드 정보 조회 및 수정, 삭제
def guild_update_delete(request, guild_pk):
    guild = get_object_or_404(Guild, pk=guild_pk)

    if request.method == 'GET':
        serializer = GuildSerializer(guild)
        return Response(serializer.data)

    if not request.user.guild_set.filter(pk=guild.pk).exists():
        return Response({'detail':'권한이 없습니다'},status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = GuildSerializer(guild, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        guild.delete()
        return Response({ 'id': guild_pk }, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
# 해당 유저의 길드 
def my_guild(request):
    if request.method == 'GET':
        myguildusers = GuildUser.objects.filter(user_id=request.user.id).order_by('-pk')
        serializer = GuildUserSerializer(myguildusers,many=True)
        return Response(serializer.data)

@api_view(['GET'])
# 해당 유저가 해당길드의 매니저인가 
def is_manager(request,guild_pk):
    if request.method == 'GET':
        guild = get_object_or_404(Guild, pk=guild_pk)
        if request.user == guild.manager:
            return Response({'is_manager':True})
        else:
            return Response({'is_manager':False})

@api_view(['GET',])
# 해당 유저가 매니저인 길드 반환
def user_manager(request):
    if request.method == 'GET':
        guilds = Guild.objects.filter(manager=request.user).order_by('-pk')
        serializer = GuildSerializer(guilds,many=True)
        return Response(serializer.data)



# signup 요청 전체 목록 반환
@api_view(['GET',])
def guild_signup_list(request):
    if request.method == 'GET':
        guildSugnups =GuildSignup.objects.all().order_by('-pk')
        serializer = GuildSignupSerializer(guildSugnups,many=True)
        return Response(serializer.data)


# signup 요청 수락 or 거절
@api_view(['DELETE','POST'])
def signup_admit_delete(request,guild_pk,user_pk):
    if request.method == 'DELETE':
        # 가입 요청 자체를 삭제함으로써 처리
        guildSignup =GuildSignup.objects.filter(guild=guild_pk,user=user_pk)
        guildSignup.delete()
        return Response({ '(user,guild)': {user_pk, guild_pk} }, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'POST':
        # 길드 유저로 기록
        signupUser = get_object_or_404(get_user_model(),pk=user_pk)
        signupGuild = get_object_or_404(Guild,pk=guild_pk)
        guildUser = GuildUser(user=signupUser,guild=signupGuild)
        guildUser.save()

        # 가입 수락 후에도 기록은 삭제
        guildSignup =GuildSignup.objects.filter(guild=guild_pk,user=user_pk)
        guildSignup.delete()

        serializer = GuildUserSerializer(guildUser)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    

@api_view(['GET','DELETE'])
# 해당 유저가 해당 길드의 유저인가 
def is_member(request,guild_pk):
    if request.method == 'GET':
        guildUsers = GuildUser.objects.filter(guild_id=guild_pk)
        print(guildUsers)
        if guildUsers.filter(user_id=request.user.id).exists():
            return Response({'isMember':True})
        else:
            return Response({'isMember':False})
    
    # 길드 탈퇴    
    elif request.method =='DELETE':
        guildUsers = GuildUser.objects.filter(guild_id=guild_pk).filter(user=request.user)
        
        guildUsers.delete()
        return Response({ 'id': request.user.id }, status=status.HTTP_204_NO_CONTENT)
        


@api_view(['GET','POST'])
def guild_signup(request,guild_pk):
    # 해당 유저가 해당 길드에 가입신청 한 사람인지
    if request.method == 'GET':
        signupUsers = GuildSignup.objects.filter(guild=guild_pk)

        if signupUsers.filter(user=request.user.id).exists():
            return Response({'isSignup':True})
        else:
            return Response({'isSignup':False})

    # 해당 유저가 해당 길드에 가입신청 
    elif request.method == 'POST':
        guildsignup = GuildSignup.objects.create(user=request.user.id, guild=guild_pk)
        serializer = GuildSignupSerializer(guildsignup)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
# 특정 길드의 글 조회 or 글 생성
def article_list_create(request,guild_pk):
    if request.method == 'GET':
        # articles = get_list_or_404(GuildArticle)
        articles = GuildArticle.objects.order_by('-pk')
        serializer = GuildArticleSerializer(articles, many=True)
        return Response(serializer.data)


    elif request.method == 'POST':
        serializer = GuildArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user = request.user)
            # print(request)
            # print(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
# 해당 길드 몇번째 글인지 
def guild_article_cnt(request,guild_pk):

    try:
        articleCnt = GuildArticleCount.objects.get(guild=guild_pk)
        count = articleCnt.cnt
        print(count)
        count += 1
        articleCnt.cnt = count
        articleCnt.save()
        
        serializer = GuildArticleCountSerializer(articleCnt)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except GuildArticleCount.DoesNotExist:
        result = GuildArticleCount.objects.create(guild=guild_pk)
        print(result)
        serializer = GuildArticleCountSerializer(result)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
   
        


@api_view(['GET',])
# 해당 유저가 작성한 글 전체 조회
def user_article(request):
    if request.method == 'GET':
        guildArticles = GuildArticle.objects.filter(user=request.user.pk).order_by('-pk')
        serializer = GuildArticleSerializer(guildArticles, many=True)
        return Response(serializer.data)



@api_view(['GET', 'POST'])
# 해당 길드에서 해당 유저가 작성한 글
def my_article(request,guild_pk):
    if request.method == 'GET':
        guildArticles = GuildArticle.objects.filter(guild_id=guild_pk).filter(user=request.user).order_by('-pk')
        # print(guildArticles)
        serializer = GuildArticleSerializer(guildArticles, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
# 해당 길드에서 해당 유저가 좋아요한 글만 조회
def my_like_article(request,guild_pk):
    if request.method == 'GET':
        guildArticles = request.user.like_articles.filter(guild_id=guild_pk).order_by('-pk')
        serializer = GuildArticleSerializer(guildArticles, many=True)
        return Response(serializer.data)

@api_view(['GET'])
# 해당 길드에서 해당 글을 해당 유저가 쓴 글인가
def is_my_guildarticle(request,guild_pk,article_pk):
    if GuildArticle.objects.filter(pk=article_pk,guild_id=guild_pk).exists():
        return Response({'isMine':True})
    else:
        return Response({'isMine':False})

# 해당 길드 특정 글 조회 수정
@api_view(['GET', 'DELETE', 'PUT'])
def article_detail(request, guild_pk, article_pk):
    
    if not request.user.guildarticle_set.filter(pk=article_pk).exists():
        return Response({'detail':'권한이 없습니다'},status=status.HTTP_403_FORBIDDEN)

    article = get_object_or_404(GuildArticle, pk=article_pk)

    if request.method == 'GET':
        serializer = GuildArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        article.delete()
        data = {
            'delete': f'데이터 {article_pk}번이 삭제되었습니다.',
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = GuildArticleSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['GET', 'POST'])
# 해당 길드의 글 타임라인에서 좋아요 수 조회 or 좋아요 클릭
def article_like(request,guild_pk,article_pk):

    # if request.user.like_articles.filter(pk=article_pk).exists():
    #     return Response({'detail':'글 작성자입니다.'},status=status.HTTP_403_FORBIDDEN)

    # article = get_object_or_404(GuildArticle, pk=article_pk)
    article = get_object_or_404(GuildArticle, pk=article_pk)
    like_user_count = article.like_users.count()
    if request.method == 'GET':
        # if request.user.like_articles.filter(pk=article_pk).exists():
        if article.like_users.filter(pk=request.user.pk).exists():
            return Response({'isLike':True,'likeUserCount' : like_user_count,})
        else:
            return Response({'isLike':False,'likeUserCount' : like_user_count,})

    elif request.method == 'POST':
        if article.like_users.filter(pk=request.user.pk).exists():
        # if request.user in article.like_users.all():
            # 좋아요 취소
            article.like_users.remove(request.user)
            is_like = False
        else:
            # 좋아요 누름
            article.like_users.add(request.user)
            is_like = True
        # return redirect('articles:index')
        # 좋아요를 누른 처리결과를 응답
        like_user_count = article.like_users.count()
        context = {
            'isLike': is_like,
            'likeUserCount' : like_user_count,
        }
        return JsonResponse(context)
    # return redirect('accounts:login')

@api_view(['GET',])
def search_guildtag(request,tag):
    # 해당 태그를 포함하는 길드 조회
    if request.method == 'GET':
        guilds = GuildTag.objects.filter(tag__contains=tag)
        serializer = GuildTagSerializer(guilds,many=True)
        print(guilds)
        return Response(serializer.data)

    


@api_view(['GET','POST'])
def guildtag_list_update(request,guild_pk):
    # 해당 길드에 태그를 추가
    if request.method == 'POST':
        guildtag = GuildTag.objects.create(tag=request.data['tag'],guild=guild_pk)
        serializer = GuildTagSerializer(guildtag)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # 해당 길드의 태그 조회
    elif request.method == 'GET':
        tags = GuildTag.objects.filter(guild=guild_pk)
        serializer = GuildTagSerializer(tags,many=True)
        return Response(serializer.data)

@api_view(['DELETE'])
def delete_tag(request,tag_pk):
    guildtag = GuildTag.objects.get(pk=tag_pk)
    guildtag.delete()
    return Response({ 'delete': f'태그 {tag_pk}번이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST','GET','DELETE'])
def like_alram(request,article_pk):
    # print(request.data)
    # print(request.user.id)
    if request.method == 'POST':
        alram = AritcleLike.objects.create(likefrom=request.data['likefrom'],likefrom_id= request.user.id,liked_article=request.data['liked_article'],liked_content=request.data['liked_content'],guild=request.data['guild'],guildname=request.data['guildname'],liketo=request.data['liketo'])
        # alram.likefrom_id = request.user.id
        serializer = AritcleLikeSerializer(alram)
        # if serializer.is_valid(raise_exception=True):
        #     serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        likealram = AritcleLike.objects.filter(liketo=request.user.pk,liked_article=article_pk)
        likealram.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['GET'])
def like_alram_list(request):
    if request.method == 'GET':
        alrams = AritcleLike.objects.filter(liketo=request.user.pk,state=0)
        serializer = AritcleLikeSerializer(alrams,many=True)
        return Response(serializer.data)