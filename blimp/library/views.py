from django.shortcuts import render, get_object_or_404, redirect
from django import template
from library.models import *
from library.serializers import *
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Count, Q, F, Value, IntegerField, Case, When, OuterRef, Subquery

import re

def home(request):
    if request.method == 'GET' and request.GET.get('query'):
    	#rank based on search terms
    	videos = Video.objects.annotate(rank=Value(0, IntegerField())) # initilize ranking with raking 0 >>> This is a start. The final system will include catagorizing step prior to posting.(details will be included in specification paper)

    	for term in re.split('\W+', request.GET.get('query')):
    		videos = videos.annotate(rank=Case(When(title__icontains=term, then=F('rank')+Value(1, IntegerField())), default=F('rank'), output_field=IntegerField())) #update rank to add 1

    	videos = videos.order_by('-rank', '-viral', '-group')

    	resultsHTML = template.loader.render_to_string('include/video_list.html', {
					'videos':videos,})

    	return JsonResponse({'search-result':resultsHTML})

    videos = Video.objects.all().order_by('-viral', '-group')

    return render(request, 'home.html', {'videos':videos})

def video_detail(request):
	vidID = request.GET.get('vidId')
	vidObj = get_object_or_404(Video, id=vidID)

	if request.method == "POST" and request.POST.get('emoji') and request.user.is_authenticated:
		emoji=Emoji.objects.get(id=request.POST.get('emoji'))
		React(text=request.POST.get('reaction'), timestamp=request.POST.get('timestamp'), emoji=emoji, video=vidObj, user=request.user).save()

	reactions = vidObj.reactions.all().order_by('-date')
	return render(request, 'video_detail.html', {'video':vidObj,
												 'reactions':reactions})

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def video_upload_api(request):
    if request.method == 'POST':
        data = {'title': request.data.get('title'), 'category': request.data.get('category'), 'user': request.user.pk, 'file': request.FILES["file"] }
        serializer = VideoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def video_detail_api(request, pk):
    video = get_object_or_404(Video, id=pk)

    if request.method == 'GET':
        serializer = VideoSerializer(video)
        return Response(serializer.data)

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


@api_view(['GET'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()

        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def category_detail(request, pk):
    category = get_object_or_404(Category, id=pk)

    if request.method == 'GET':
        serializer = CategoryEmojiSerializer(category)
        return Response(serializer.data)
