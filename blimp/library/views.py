from django.shortcuts import render, get_object_or_404
from django import template
from library.models import *
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Q, F, Value, IntegerField, Case, When, OuterRef, Subquery


import re

def home(request):
    if request.method == 'POST':
        file = request.FILES["file"]
        title = request.POST.get("title")

        if file.name.endswith('.mp4'):
            Video(file=file, title=title).save()
        elif file._size > 10485760:
            messages.error(request,'File size too DARN big *_*')
        else:
            messages.error(request,'File is not of video type')
    elif request.method == 'GET' and request.GET.get('query'):
    	#rank based on search terms
    	videos = Video.objects.annotate(rank=Value(0, IntegerField())) # initilize ranking with raking 0 >>> This is a start. The final system will include catagorizing step prior to posting.(details will be included in specification paper)

    	for term in re.split('\W+', request.GET.get('query')):
    		videos = videos.annotate(rank=Case(When(title__icontains=term, then=F('rank')+Value(1, IntegerField())), default=F('rank'), output_field=IntegerField())) #update rank to add 1

    	videos = videos.order_by('-rank')

    	for v in videos:
    		print(v.rank)

    	resultsHTML = template.loader.render_to_string('include/video_list.html', {
					'videos':videos,})

    	return JsonResponse({'search-result':resultsHTML})

    videos = Video.objects.all()

    return render(request, 'home.html', {'videos':videos})

def video_detail(request):
	vidID = request.GET.get('vidId')
	vidObj = get_object_or_404(Video, id=vidID)

	if request.method == "POST" and request.POST.get('reaction') and request.user.is_authenticated:
		React(raw=request.POST.get('reaction'), video=vidObj, user=request.user).save()

	reactions = vidObj.reactions.all().order_by('-date')

	return render(request, 'video_detail.html', {'video':vidObj,
												 'reactions':reactions})