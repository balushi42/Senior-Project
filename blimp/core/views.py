from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from core.serializers import *

# Create your views here.
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def profile(request):
	return render(request, 'registration/profile.html', {})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile_api(request):
    if request.method == 'GET':
        serializer = ProfileSerializer(request.user.profile)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def friends_api(request):
    if request.method == 'GET':
        serializer = FriendSerializer(request.user.profile.friends(), many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        friend = User.objects.get(pk=request.data.get('friend'))
        data = {'creator':request.user.pk, 'friend':friend.pk}
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