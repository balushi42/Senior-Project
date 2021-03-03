from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
	file = models.FileField(null=False, blank=False)
	title = models.CharField(max_length=50)
	date_uploaded = models.DateTimeField(auto_now_add=True)

class React(models.Model):
	raw = models.CharField(max_length=50)
	video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="reactions")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reactions")
	date = models.DateTimeField(auto_now_add=True)