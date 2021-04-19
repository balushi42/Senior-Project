from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Avg, Max, Min, F, ExpressionWrapper, FloatField

from library.models import *
from core.serializers import *

import datetime
from datetime import timedelta
import pytz

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile_api(request):
    if request.method == 'GET':
        serializer = ProfileSerializer(request.user.profile)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def logout_api(request):
    if request.method == 'GET':
        return Response()

@api_view(['GET'])
def people_api(request):
    if request.method == 'GET':
        serializer = ProfileSerializer(Profile.objects.all(), many=True)
        return Response(serializer.data)

@api_view(['GET'])
def people_detail_api(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def friends_api(request):
    if request.method == 'GET':
        serializer = FriendSerializer(request.user.profile.friends(), many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        friend = User.objects.get(pk=request.data.get('friend'))
        data = {'creator':request.user.pk, 'friend':friend.pk, 'status': Friendship.PENDING}
        serializer = FriendSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def friends_pending_api(request):
    if request.method == 'GET':
        serializer = FriendSerializer(request.user.profile.friends_pending(), many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        friend_request = request.user.profile.friends_pending().get(friend=request.user.pk, creator=request.data.get('friend'))
        data = {'friend':request.user.pk, 'creator':friend_request.creator.pk, 'status':Friendship.ACCEPTED}
        serializer = FriendSerializer(friend_request, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CreateUserView(CreateAPIView):

    model = User
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


def Chart_Detail_View(request,pk):
    video = get_object_or_404(Video, id=pk)
    date_delta = timedelta(days=1)

    labels = []
    PHI_data = []
    PLI_data = []
    NHI_data = []
    NLI_data = []

    start_date = video.date_uploaded
    end_date = datetime.datetime.now(tz=pytz.utc)

    last = False
    while not last:
        if start_date >= end_date:
            last = True
        labels.append(start_date)
        PHI_data.append(React.objects.filter(emoji__in=video.category.PHI.all(), video=video, date__lte=start_date).count())
        PLI_data.append(React.objects.filter(emoji__in=video.category.PLI.all(), video=video, date__lte=start_date).count())
        NHI_data.append(React.objects.filter(emoji__in=video.category.NHI.all(), video=video, date__lte=start_date).count())
        NLI_data.append(React.objects.filter(emoji__in=video.category.NLI.all(), video=video, date__lte=start_date).count())
        start_date += date_delta
    return render(request, 'Charts.html', {"video":video,'labels':labels,'PHI_data':PHI_data,"PLI_data":PLI_data,"NHI_data":NHI_data,"NLI_data":NLI_data})

def Chart_Viral_View(request,pk):
    video = get_object_or_404(Video, id=pk)
    avg_vval = video.category.videos.aggregate(Avg('viral'))['viral__avg']

    date_delta = timedelta(days=1)

    labels = []
    vval_data = []
    avg_vval_data = []

    start_date = video.date_uploaded
    end_date = datetime.datetime.now(tz=pytz.utc)

    last = False
    while not last:
        if start_date >= end_date:
            last = True
        labels.append(start_date)
        
        PHI_count = React.objects.filter(emoji__in=video.category.PHI.all(), video=video, date__lte=start_date).count()
        PLI_count = React.objects.filter(emoji__in=video.category.PLI.all(), video=video, date__lte=start_date).count()
        NHI_count = React.objects.filter(emoji__in=video.category.NHI.all(), video=video, date__lte=start_date).count()
        NLI_count = React.objects.filter(emoji__in=video.category.NLI.all(), video=video, date__lte=start_date).count()
        
        PHI_avg_count = React.objects.filter(emoji__in=video.category.PHI.all(), video__category=video.category, date__lte=start_date).count()/video.category.videos.all().count()
        PLI_avg_count = React.objects.filter(emoji__in=video.category.PLI.all(), video__category=video.category, date__lte=start_date).count()/video.category.videos.all().count()
        NHI_avg_count = React.objects.filter(emoji__in=video.category.NHI.all(), video__category=video.category, date__lte=start_date).count()/video.category.videos.all().count()
        NLI_avg_count = React.objects.filter(emoji__in=video.category.NLI.all(), video__category=video.category, date__lte=start_date).count()/video.category.videos.all().count()

        vval_data.append(PHI_count*video.category.PHI_Vdelta+PLI_count*video.category.PLI_Vdelta+NHI_count*video.category.NHI_Vdelta+NLI_count*video.category.NLI_Vdelta)
        avg_vval_data.append(PHI_avg_count*video.category.PHI_Vdelta+PLI_avg_count*video.category.PLI_Vdelta+NHI_avg_count*video.category.NHI_Vdelta+NLI_avg_count*video.category.NLI_Vdelta)

        start_date += date_delta
    return render(request, 'Vval_Chart.html', {"video":video,'labels':labels,'vval_data':vval_data,"avg_vval_data":avg_vval_data,"avg_vval":avg_vval})

def Chart_Group_View(request,pk):
    video = get_object_or_404(Video, id=pk)
    avg_gval = video.category.videos.aggregate(Avg('viral'))['viral__avg']

    date_delta = timedelta(hours=1)

    labels = []
    gval_data = []
    avg_gval_data = []

    start_date = video.date_uploaded
    end_date = datetime.datetime.now(tz=pytz.utc)

    last = False
    while not last:
        if start_date >= end_date:
            last = True
        labels.append(start_date)
        
        PHI_count = React.objects.filter(emoji__in=video.category.PHI.all(), video=video, date__lte=start_date).count()
        PLI_count = React.objects.filter(emoji__in=video.category.PLI.all(), video=video, date__lte=start_date).count()
        NHI_count = React.objects.filter(emoji__in=video.category.NHI.all(), video=video, date__lte=start_date).count()
        NLI_count = React.objects.filter(emoji__in=video.category.NLI.all(), video=video, date__lte=start_date).count()
        
        PHI_avg_count = React.objects.filter(emoji__in=video.category.PHI.all(), video__category=video.category, date__lte=start_date).count()/video.category.videos.all().count()
        PLI_avg_count = React.objects.filter(emoji__in=video.category.PLI.all(), video__category=video.category, date__lte=start_date).count()/video.category.videos.all().count()
        NHI_avg_count = React.objects.filter(emoji__in=video.category.NHI.all(), video__category=video.category, date__lte=start_date).count()/video.category.videos.all().count()
        NLI_avg_count = React.objects.filter(emoji__in=video.category.NLI.all(), video__category=video.category, date__lte=start_date).count()/video.category.videos.all().count()

        gval_data.append(PHI_count*video.category.PHI_Gdelta+PLI_count*video.category.PLI_Gdelta+NHI_count*video.category.NHI_Gdelta+NLI_count*video.category.NLI_Gdelta)
        avg_gval_data.append(PHI_avg_count*video.category.PHI_Gdelta+PLI_avg_count*video.category.PLI_Gdelta+NHI_avg_count*video.category.NHI_Gdelta+NLI_avg_count*video.category.NLI_Gdelta)

        start_date += date_delta
    return render(request, 'Gval_Chart.html', {"video":video,'labels':labels,'gval_data':gval_data,"avg_gval_data":avg_gval_data,"avg_gval":avg_gval})

def Chart_View(request):
    videos = Video.objects.all()
    avg_viral = videos.aggregate(Avg('viral'))
    max_viral = videos.order_by('-viral').first().viral-avg_viral['viral__avg']
    min_viral = videos.order_by('viral').first().viral-avg_viral['viral__avg']
    videos = videos.annotate(vscore=ExpressionWrapper((F('viral')-avg_viral['viral__avg']-min_viral)/(max_viral-min_viral), output_field=FloatField()))
    print((videos.first().viral,avg_viral['viral__avg'],min_viral,max_viral))
    return render(request, 'Content_Chart.html', {"videos":videos})


def Chart_Category_View(request,pk):
    category = get_object_or_404(Category,pk=pk)
    videos = Video.objects.filter(category=category)
    return render(request, 'Category_Chart.html', {"videos":videos})


