from django.shortcuts import render, get_object_or_404
from django import template
from library.models import *
from library.serializers import *
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q, F, Value, IntegerField, Case, When

import re

#api method to serialize videos and perform queries
@api_view(['GET'])
def video_list(request):
    if request.method == 'GET':
        if request.GET.get('query'):
            videos = Video.objects.annotate(rank=Value(0, IntegerField())) # initilize ranking with raking 0 >>> This is a start. The final system will include catagorizing step prior to posting.(details will be included in specification paper)
            for term in re.split('\W+', request.GET.get('query')):
                videos = videos.annotate(rank=Case(When(title__icontains=term, then=F('rank')+Value(1, IntegerField())), default=F('rank'), output_field=IntegerField())) #update rank to add 1
            videos = videos.order_by('-rank', '-viral', '-group')
        else:
            videos = Video.objects.all().order_by('-viral', '-group')

        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

#api method to serialize videos of current user and friends in order of newest first and by their viral and group rank
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def timeline_api(request):
    if request.method == 'GET':
        videos = Video.objects.filter(Q(user=request.user) | Q(user__friendship_creator_set__friend=request.user) | Q(user__friend_set__creator=request.user) | Q(reactions__user=request.user) | Q(reactions__user__friendship_creator_set__friend=request.user) | Q(reactions__user__friend_set__creator=request.user)).distinct()
        videos = videos.order_by('-date_uploaded', '-viral', '-group')

        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

#api method to serialize videos of current user and friends in order of newest first and by their viral and group rank
@api_view(['GET'])
def viral_timeline_api(request):
    if request.method == 'GET':
        videos = Video.objects.all().order_by('-viral', '-date_uploaded', '-group')

        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

#api method to handle uploading file to timeline
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def video_upload_api(request):
    if request.method == 'POST':
        try:
            data = {'title': request.data.get('title'), 'category': request.data.get('category'), 'user': request.user.pk, 'file': request.FILES["file"] }
        except MultiValueDictKeyError:
            data = {'title': request.data.get('title'), 'category': request.data.get('category'), 'user': request.user.pk, 'file': None }
        serializer = VideoUploadSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#api method to retrive single serialized video object
@api_view(['GET'])
def video_detail_api(request, pk):
    video = get_object_or_404(Video, id=pk)

    if request.method == 'GET':
        serializer = VideoSerializer(video)
        return Response(serializer.data)

#api method to retrieve video reactions(anon) and post a new reaction(user)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def video_reactions_api(request, pk):
    video = get_object_or_404(Video, id=pk)

    if request.method == 'GET':
        serializer = VideoReactionSerializer(video)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = {'emoji': request.data.get('emoji'), 'text': request.data.get('text'),'timestamp': request.data.get('timestamp'), 'user':request.user.pk, 'video':video.pk}
        serializer = ReactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#api method to retrive available categories
@api_view(['GET'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()

        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

#api method to retrive specific category
@api_view(['GET'])
def category_detail(request, pk):
    category = get_object_or_404(Category, id=pk)

    if request.method == 'GET':
        serializer = CategoryEmojiSerializer(category)
        return Response(serializer.data)
