from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    PHI_Gdelta = models.IntegerField(default=10)
    PLI_Gdelta = models.IntegerField(default=5)
    NHI_Gdelta = models.IntegerField(default=0)
    NLI_Gdelta = models.IntegerField(default=-10)
    
    PHI_Vdelta = models.IntegerField(default=10)
    PLI_Vdelta = models.IntegerField(default=0)
    NHI_Vdelta = models.IntegerField(default=5)
    NLI_Vdelta = models.IntegerField(default=-10)
    
    def __str__(self):
        return self.title

class Video(models.Model):
    category = models.ForeignKey(Category,related_name="videos", on_delete=models.CASCADE)
    file = models.FileField(null=False, blank=False)
    title = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="videos")
    date_uploaded = models.DateTimeField(auto_now_add=True)
    group = models.IntegerField(default=0)
    viral = models.IntegerField(default=0)
    def getGrpVal(self):
        PHI = React.objects.filter(emoji__in=self.category.PHI.all(), video=self).count()
        PLI = React.objects.filter(emoji__in=self.category.PLI.all(), video=self).count()
        NHI = React.objects.filter(emoji__in=self.category.NHI.all(), video=self).count()
        NLI = React.objects.filter(emoji__in=self.category.NLI.all(), video=self).count()
        return PHI*self.category.PHI_Gdelta+PLI*self.category.PLI_Gdelta+NHI*self.category.NHI_Gdelta+NLI*self.category.NLI_Gdelta

    def getVirVal(self):
        PHI = React.objects.filter(emoji__in=self.category.PHI.all(), video=self).count()
        PLI = React.objects.filter(emoji__in=self.category.PLI.all(), video=self).count()
        NHI = React.objects.filter(emoji__in=self.category.NHI.all(), video=self).count()
        NLI = React.objects.filter(emoji__in=self.category.NLI.all(), video=self).count()
        return PHI*self.category.PHI_Vdelta+PLI*self.category.PLI_Vdelta+NHI*self.category.NHI_Vdelta+NLI*self.category.NLI_Vdelta

    
class React(models.Model):
    emoji = models.ForeignKey(Emoji, on_delete=models.PROTECT, related_name="reactions")
    text = models.CharField(max_length=50)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reactions")
    date = models.DateTimeField(auto_now_add=True)
    timestamp = models.TimeField(blank=False,null=False)

@receiver(post_save, sender=React)
def updateGrpVal(sender, instance, **kwargs):
    instance.video.group = instance.video.getGrpVal()
    instance.video.viral = instance.video.getVirVal()
    instance.video.save()