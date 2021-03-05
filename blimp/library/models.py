from django.db import models
from django.contrib.auth.models import User


class Emoji(models.Model):
    text = models.CharField(max_length=10)
    def __str__(self):
        return self.text
    

class Category(models.Model):
    title = models.CharField(max_length=50)
    PHI = models.ManyToManyField(Emoji, related_name="PHI_catagories")
    PLI = models.ManyToManyField(Emoji, related_name="PLI_catagories")
    NHI = models.ManyToManyField(Emoji, related_name="NHI_catagories")
    NLI = models.ManyToManyField(Emoji, related_name="NLI_catagories")
    def __str__(self):
        return self.title

class Video(models.Model):
    category = models.ForeignKey(Category,related_name="videos", on_delete=models.CASCADE)
    file = models.FileField(null=False, blank=False)
    title = models.CharField(max_length=50)
    date_uploaded = models.DateTimeField(auto_now_add=True)

class React(models.Model):
    emoji = models.ForeignKey(Emoji, on_delete=models.PROTECT)
    text = models.CharField(max_length=50)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reactions")
    date = models.DateTimeField(auto_now_add=True)
    timestamp = models.TimeField(blank=False,null=False)