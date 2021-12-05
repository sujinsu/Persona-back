from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


from .serializers import BalanceGameSerializer

from .models import BalanceGame
# Create your views here.
import random
from django.db.models import Max
@api_view(['GET'])
@permission_classes([AllowAny])
def balanceGame(request):
    if request.method =='GET':
        max_id = BalanceGame.objects.all().aggregate(Max('pk'))
        # print(max_id)
        random_pk = random.randint(1,max_id['pk__max'])
        # print(random_pk)
        balancegame =  BalanceGame.objects.get(pk=random_pk)
        serializer = BalanceGameSerializer(balancegame)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def vote_update(request,pk):
    if request.method =='GET':
        balancegame = BalanceGame.objects.get(pk=pk)
        
        serializer = BalanceGameSerializer(balancegame)
        return Response(serializer.data)

@api_view(['PUT'])
def game_vote(request):
    print(request.data)
    
    balancegame =  BalanceGame.objects.get(pk=request.data['id'])
    if request.method == 'PUT':
        serializer = BalanceGameSerializer(balancegame, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
