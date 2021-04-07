from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from library.models import *
from core.serializers import *

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


def Chart_View(request,pk):
    video = get_object_or_404(Video, id=pk)
    PHI = React.objects.filter(emoji__in=video.category.PHI.all(), video=video).count()
    PLI = React.objects.filter(emoji__in=video.category.PLI.all(), video=video).count()
    NHI = React.objects.filter(emoji__in=video.category.NHI.all(), video=video).count()
    NLI = React.objects.filter(emoji__in=video.category.NLI.all(), video=video).count()
    return render(request, 'Charts.html', {'PHI_VAL':PHI,"PLI_VAL":PLI,"NHI_VAL":NHI,"NLI_VAL":NLI})