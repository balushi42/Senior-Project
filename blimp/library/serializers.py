from rest_framework import serializers
from .models import Video


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = ('id', 'title', 'category', 'date_uploaded', 'file')
        read_only_fields = ('id', 'title', 'category', 'date_uploaded', 'file')
