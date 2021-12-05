from django.contrib.auth import get_user_model
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http.response import JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny

from movies.models import Movie, Review, Form, Collection, Tag
from .serializers import CollectionUpdateSerializer, MovieSerializer, MovieUpdateSerializer, ReviewSerializer, FormSerializer, CollectionSerializer, TagSerializer
from accounts.serializers import UserSerializer

from django.db.models import Count
import random
# Create your views here.


# 사용자에게 영화 추천을 해주기 위해서 영화 선택지를 줌
@api_view(['GET', 'POST'])
def movie_recommendation(request):
    total = len(Movie.objects.all())
    randomNum = random.sample(range(1,total), 10)
    randomMovies = Movie.objects.filter(id__in=randomNum)
    serializer = MovieSerializer(randomMovies, many=True)
    return Response(serializer.data)


# admin이 영화를 DB에 저장하는 함수 ('POST')
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def movie_list_and_create(request, val):
    # 관리자이면 영화등록 가능
    # 등록된 영화 전체 조회
    if request.method == 'GET':
        # 등록순 정렬 요청이 들어오면
        if val == 1:
            movies = Movie.objects.order_by('-created_at')
        # 인기순 정렬 요청이 들어오면
        elif val == 2:
            movies = Movie.objects.annotate(Count('like_users')).order_by('-like_users__count')
        # 조회순 정렬 요청이 들어오면
        else: 
            movies = Movie.objects.order_by('-hits')
        serializer = MovieSerializer(movies, many=True)	
        return Response(serializer.data)
    else:
        if request.user.is_superuser and request.user.is_authenticated:
            api_id = request.data.get('api_id')
            try:
                movie = Movie.objects.get(api_id=api_id)
            except Movie.DoesNotExist:
                serializer = MovieSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response()


# 등록된 영화 수정/삭제하기 (admin권한)
@api_view(['PUT', 'DELETE'])
def movie_update_and_delete(request, api_id):
    if request.user.is_superuser:
        movie = get_object_or_404(Movie, api_id=api_id)
        # 수정하기(영화 overview, poster_path, release_date, title만 수정 가능하도록)
        if request.method == 'PUT':
            serializer = MovieUpdateSerializer(movie, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            
        # 삭제
        elif request.method == 'DELETE':
            title = movie.title
            movie.delete()
            data = {
                'delete': f'영화 [{title}] (이)가 삭제되었습니다.'
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)


# DB에 있는 영화인 경우 영화의 상세 내용을 반환
# 없는 경우 title을 빈 값으로 반환
@api_view(['GET'])
@permission_classes([AllowAny])
def movie_detail(request, api_id):
    try:
        movie = Movie.objects.get(api_id=api_id)
        movie.hits += 1
        movie.save()
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Movie.DoesNotExist:
        return Response({'title':''})


# 영화 등록을 요청하는 모든 폼들을 반환하는 함수 ('GET')
# 영화 등록을 요청하는 폼을 저장하는 함수 ('POST')
@api_view(['GET', 'POST'])
def request_list_and_create(request):
    if request.method == 'GET':
        # admin만 요청들어온 폼 볼 수 있음
        if request.user.is_superuser:
            try: 
                forms = Form.objects.all()
                serializer = FormSerializer(forms, many=True)
                return Response(serializer.data)
            except Form.DoesNotExist:
                return Response()

    elif request.method == 'POST':
        serializer = FormSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 영화 등록 요청 폼 삭제
@api_view(['DELETE'])
def delForm(request, form_pk):
    form = get_object_or_404(Form, pk=form_pk)
    form.delete()
    return Response(status=status.HTTP_200_OK)

# 해당 영화를 좋아요한 유저들을 반환하는 함수 ('GET')
# 현재 로그인한 유저가 해당 영화에 좋아요하거나 좋아요 취소할 수 있는 함수 ('POST')
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def like_cnt_and_create(request, movie_pk):
    if request.method == 'GET':
        movie = get_object_or_404(Movie, pk=movie_pk)
        user_cnt = movie.like_users.count()
        return Response({'user_cnt':user_cnt})

    # 영화 좋아요 표시
    if request.user.is_authenticated:
        if request.method == 'POST':
            movie = get_object_or_404(Movie, pk=movie_pk)
            if movie.like_users.filter(pk=request.user.pk).exists():
                movie.like_users.remove(request.user)
                isLiked = False
            else:
                movie.like_users.add(request.user)
                isLiked = True
            context = {
                'isLiked': isLiked
            }
            return JsonResponse(context)


# 해당 영화의 리뷰들을 반환하는 함수 ('GET')
# 해당 영화의 리뷰를 생성하는 함수 ('POST')
@api_view(['GET', 'POST'])
def review_list_and_create(request, movie_pk):
    if request.method == 'GET':
        if Review.objects.filter(movie=movie_pk).exists():
            reviews = get_list_or_404(Review, movie=movie_pk)
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data)
        else:
            return Response()
        
    elif request.method == 'POST':
        # movie 모델에서 vote_average 다시 계산
        movie = get_object_or_404(Movie, pk=movie_pk)
        total = movie.vote_average * movie.vote_count
        movie.vote_count += 1
        movie.vote_average = round((total + int(request.data['rating']))/movie.vote_count, 2)
        print(movie.vote_average)
        movie.save()
        print(movie.vote_average)
        # review 저장하기
        review = Review.objects.create(user=request.user, movie=movie, content=request.data['content'])
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 현재 로그인한 유저가 해당 영화(movie_pk)를 좋아요 했는지 여부를 확인하는 함수
@api_view(['POST'])
def isLiked(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    # 해당 영화를 request.user가 좋아요 했다면
    if movie.like_users.filter(pk=request.user.pk).exists():
        isLiked = True
    else:
        isLiked = False
    context = {
        'isLiked': isLiked
    }
    return JsonResponse(context)


# 해당 영화가 DB에 있는 영화인지 확인하는 함수
@api_view(['POST'])
@permission_classes([AllowAny])
def isInDB(request, api_id):
    try:
        Movie.objects.get(api_id=api_id)
        isInDB = True
    except Movie.DoesNotExist:
        isInDB = False
    return Response({'isInDB': isInDB})


# 리뷰쓴 유저의 username과 id를 반환하는 함수
@api_view(['GET'])
@permission_classes([AllowAny])
def get_review_user(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    user = review.user
    context = {
        'username': user.username,
        'user_id': user.id,
    }
    return JsonResponse(context)


# review를 좋아요한 유저들을 반환하는 함수 ('GET")
# 현재 로그인한 유저가 리뷰에 좋아요하거나 좋아요 취소를 하는 함수 ('POST')
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def review_like_cnt_and_create(request,review_pk):
    if request.method == 'GET':
        review = get_object_or_404(Review, pk=review_pk)
        user_cnt = review.like_users.count()
        return Response({'user_cnt':user_cnt})

    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                review = get_object_or_404(Review, pk=review_pk)
                if review.like_users.filter(pk=request.user.pk).exists():
                    review.like_users.remove(request.user)
                    isReviewLiked= False
                else:
                    review.like_users.add(request.user)
                    isReviewLiked= True
                context = {
                    'isReviewLiked': isReviewLiked
                }
                return JsonResponse(context)
            except Review.DoesNotExist:
                return Response({'err':'없는 객체'})


# 로그인된 유저가 해당 영화 리뷰를 좋아요 했는지 여부 확인하는 함수
@api_view(['POST'])
def isReviewLiked(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if review.like_users.filter(pk=request.user.pk):
        isReviewLiked = True
    else:
        isReviewLiked = False
    context = {
        'isReviewLiked': isReviewLiked
    }
    return JsonResponse(context)


# keyword로 DB에 있는 영화 찾는 함수
@api_view(['GET'])
@permission_classes([AllowAny])
def searchKeyword(request, keyword):
    movies = Movie.objects.filter(title__contains=keyword)
    # print(movies)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


# collection 만드는 함수
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def collections_list_and_create(request, val):
    if request.method == 'GET':
        if val == 1:
            collections = Collection.objects.order_by('-updated_at')
        else:
            collections = Collection.objects.annotate(Count('like_users')).order_by('-like_users__count')
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if request.user.is_authenticated:
            title = request.data['title']
            content = request.data['content']
            movies = request.data['movies']
            tags = request.data['tags']

            collection = Collection.objects.create(user=request.user, 
                        title=title, content=content)
            for movie in movies:
                collection.movies.add(movie)
            serializer = CollectionSerializer(collection)
            
            for tag in tags:
                Tag.objects.create(tag=tag, collection=collection)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

# 현재 유저가 해당 컬렉션을 좋아요 했는지 여부 확인
@api_view(['POST'])
def isCollectionLiked(request, collection_pk):
    collection = get_object_or_404(Collection, pk=collection_pk)
    print(collection)
    if collection.like_users.filter(pk=request.user.pk):
        isCollectionLiked = True
    else:
        isCollectionLiked = False
    return Response({'isCollectionLiked': isCollectionLiked})


# 해당 컬렉션을 좋아요한 유저들 반환('GET')
# 해당 컬렉션 좋아요 또는 좋아요 취소('POST')
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def collection_like_cnt_and_create(request, collection_pk):
    if request.method == 'GET':
        collection = get_object_or_404(Collection, pk=collection_pk)
        user_cnt = collection.like_users.count()
        return Response({'user_cnt':user_cnt})

    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                collection = get_object_or_404(Collection, pk=collection_pk) 
                if collection.like_users.filter(pk=request.user.pk).exists():
                    collection.like_users.remove(request.user)
                    isCollectionLiked = False
                else:
                    collection.like_users.add(request.user)
                    isCollectionLiked = True
                return Response({'isCollectionLiked': isCollectionLiked})
            except Collection.DoesNotExist:
                return Response({'err': '없는 객체'})


# 컬렉션 검색(제목)
@api_view(['GET'])
@permission_classes([AllowAny])
def search_collection_title(request, keyword):
    collections = Collection.objects.filter(title__contains=keyword)
    serializer = CollectionSerializer(collections, many=True)

    tags = Tag.objects.exclude(collection__in=collections)
    tags = tags.filter(tag__contains=keyword)

    return Response(serializer.data)


# 컬렉션 검색(태그)
@api_view(['GET'])
@permission_classes([AllowAny])
def search_collection_tag(request, keyword):
    # tag 검색 결과와 collection의 검색결과가 겹치지 않게 set 이용
    collections = Collection.objects.filter(title__contains=keyword)
    collection_id = set()
    for collection in collections:
        collection_id.add(collection.id)

    tags = Tag.objects.filter(tag__contains=keyword)
    for tag in tags:
        collection_id.add(tag.collection.id)
    
    results = get_list_or_404(Collection, pk__in=collection_id)
    
    serializer = CollectionSerializer(results, many=True)
    return Response(serializer.data)


# 해당 collection_pk에 해당하는 collection json으로 반환
@api_view(['GET'])
@permission_classes([AllowAny])
def get_collect_json(request, collection_pk):
    try:
        collection = Collection.objects.get(pk=collection_pk)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    except:
        return Response()



@api_view(['POST'])
@permission_classes([AllowAny])
# 해당 컬렉션을 만든 유저와 로그인된 유저가 같은지 확인
def is_collection_user(request, collection_pk):
    collection = get_object_or_404(Collection, pk=collection_pk)
    collection_user = collection.user
    if request.user == collection_user:
        isSame = True
    else:
        isSame = False
    context = {
        'isSame': isSame,
    }
    return JsonResponse(context)



@api_view(['PUT', 'DELETE'])
# 해당 컬렉션 수정 및 삭제
def collection_update_and_delete(request, collection_pk):
    collection = get_object_or_404(Collection, pk=collection_pk)
    if request.method == 'PUT':
        collection.title = request.data['title']
        collection.content = request.data['content']
        movies = request.data['movies']
        tags = request.data['tags']
        collection.save()

        collection.movies.clear()
        for movie in movies:
            collection.movies.add(movie['id'])

        Tag.objects.filter(collection=collection_pk).delete()
        for tag in tags:
                Tag.objects.create(tag=tag, collection=collection)
        
        result = Collection.objects.get(pk=collection_pk)
        serializer = CollectionSerializer(result)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    elif request.method == 'DELETE':
        collection = get_object_or_404(Collection, pk=collection_pk)
        collection.delete()
        data = {
                'delete': f'해당 컬렉션이 삭제되었습니다.'
                }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_collection_tags(request, collection_pk):
    tags = Tag.objects.filter(collection=collection_pk)
    serializer = TagSerializer(tags, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_my_likes(request, val):
    user = get_object_or_404(get_user_model(), pk=request.user.pk)
    # val == 2이면 내가 좋아요한 영화 리스트
    if val == 2:
        movies = user.like_movies.all()
        serializer = MovieSerializer(movies, many=True)
    
    # 내가 좋아요한 컬렉션 리스트
    elif val == 3:
        collections = user.like_collections.all()
        serializer = CollectionSerializer(collections, many=True)

    return Response(serializer.data)
