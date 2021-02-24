from django.shortcuts import render
from library.models import *
from django.contrib import messages

def home(request):
    if request.method == 'POST':
        file = request.FILES["file"]

        if file.name.endswith('.mp4'):
            Video(file=file).save()
        else:
            messages.error(request,'File is not of video type')

    videos = Video.objects.all()

    return render(request, 'home.html', {'videos':videos})