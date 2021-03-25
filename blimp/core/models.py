from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models import Q
from library.models import Video

class Friendship(models.Model):
	#possible states
	PENDING = 1
	ACCEPTED = 2

	FRIENDSHIP_STATUS = ((PENDING, 'Pending'),
			(ACCEPTED, 'Accepted'),)

	created = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(choices=FRIENDSHIP_STATUS, default=PENDING)
	creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friendship_creator_set")
	friend = models.ForeignKey(User,  on_delete=models.CASCADE, related_name="friend_set")

class Profile(models.Model):
	user =  models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username + " Profile"
	def videos(self):
		return self.user.videos.all()
	def friends(self):
		return Friendship.objects.filter(Q(creator=self.user, status=Friendship.ACCEPTED)|Q(friend=self.user, status=Friendship.ACCEPTED)).all()
	def friends_pending(self):
		return Friendship.objects.filter(Q(creator=self.user, status=Friendship.PENDING)|Q(friend=self.user, status=Friendship.PENDING)).all()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
	    Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

	
class videoView(models.Model):
	user =  models.OneToOneField(User, on_delete=models.CASCADE)
	video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="videoViews")
	date_viewed = models.DateTimeField(auto_now_add=True)
