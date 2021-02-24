from django.db import models

class Video(models.Model):
    file = models.FileField(null=False, blank=False)
    title = models.CharField(max_length=50)
    date_uploaded = models.DateTimeField(auto_now_add=True)
