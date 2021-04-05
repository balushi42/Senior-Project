from rest_framework import serializers
from library.exceptions import *
from .models import Video, React, Category, Emoji
from core.serializers import *


class CategorySerializer(serializers.ModelSerializer):

	class Meta:
		model = Category
		fields = ['id', 'title']
		read_only_fields = ['id', 'title']

class VideoSerializer(serializers.ModelSerializer):
	def validate(self, data):
		file = data['file']
		if not (file.name.endswith('.mp4') or file.name.endswith('.m4v')):
			raise InvalidFileFormat()
		elif file.size > 10485760:
			raise LargeFileSize()
		return data

	user = UserSerializer()
	category = CategorySerializer(read_only=True, many=True)
	class Meta:
		model = Video
		fields = ('id', 'title', 'category', 'user', 'date_uploaded', 'file')


class ReactionSerializer(serializers.ModelSerializer):

	def validate(self, data):
		#test emoji valid within video category
		category = data['video'].category
		if category.PHI.filter(text=data['emoji']).count() == 0 and category.PLI.filter(text=data['emoji']).count() == 0 and category.NHI.filter(text=data['emoji']).count() == 0 and category.NLI.filter(text=data['emoji']).count() == 0:
			raise serializers.ValidationError({"emoji": "emoji selection error, category does not support this choice"})
		return data

	class Meta:
		model = React
		fields = ('emoji', 'text', 'user', 'timestamp', 'date', 'video')

class VideoReactionSerializer(serializers.ModelSerializer):

	reactions = ReactionSerializer(many=True)

	class Meta:
		model = Video
		fields = ('reactions',)



class EmojiSerializer(serializers.ModelSerializer):

	class Meta:
		model = Emoji
		fields = ('__all__')
		read_only_fields = ['__all__']

class CategoryEmojiSerializer(serializers.ModelSerializer):

	PHI = EmojiSerializer(many=True)
	PLI = EmojiSerializer(many=True)
	NHI = EmojiSerializer(many=True)
	NLI = EmojiSerializer(many=True)

	class Meta:
		model = Category
		fields = ('PHI', 'PLI', 'NHI', 'NLI', )
