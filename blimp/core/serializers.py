from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import Profile, Friendship
from django.db.models import Q


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        Illegal_chars = ['@',]
        for c in Illegal_chars:
            if c in validated_data['username']:
                raise serializers.ValidationError({"username": "Username selection cannot contain illegal characters"})

        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['user']

class FriendSerializer(serializers.ModelSerializer):
    def validate(self, data):
        #test friend make sure no duplicate
        friend = data['friend']
        creator = data['creator']
        status = data['status']
        if status == Friendship.PENDING and Friendship.objects.filter(Q(creator=creator, friend=friend)|Q(friend=creator, creator=friend)).count() != 0:
            raise serializers.ValidationError({"friend": "Friend selection error, Already friends/pending"})
        elif status == Friendship.ACCEPTED and Friendship.objects.filter(creator=creator, friend=friend).count() != 1:
            raise serializers.ValidationError({"friend": "Friend selection error, selected request not found"})
        elif friend == creator:
            raise serializers.ValidationError({"friend": "Friend selection error, cannot friend self"})

        return data
    class Meta:
        model = Friendship
        fields = ['creator', 'friend', 'status']
