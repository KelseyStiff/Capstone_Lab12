from django.shortcuts import render, redirect
from .forms import VideoForm, SearchForm
from django.contrib import messages
from .models import Video
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models.functions import Lower


# Create your views here.

def home(request):
    app_name = 'Lofi Videos' 
    return render(request, 'video_collection/home.html', {'app_name': app_name})


def add(request):
    if request.method == "POST":
        new_video_form = VideoForm(request.POST)
        if new_video_form.is_valid:
            try:
                new_video_form.save()
                return redirect('video_list')
                # todo show success message or redirect to list of videos
                # messages.info(request, 'New video saved!')
            
            except ValidationError:
                messages.warning(request, 'Invalid Youtube Url')
            except IntegrityError:
                messages.warning(request, 'This Video has already been added')
    
        messages.warning(request, 'please check data entered')
        return render(request, 'video_collection/add.html', {'new_video_form': new_video_form })

    new_video_form = VideoForm()
    return render(request, 'video_collection/add.html', {'new_video_form': new_video_form })


def video_list(request):
    search_form = SearchForm(request.GET) #build form from data user sent to app

    if search_form.is_valid():
        search_term = search_form.cleaned_data['search_term'] #example: 'animal crossing lofi' or 'Zelda lofi
        videos = Video.objects.filter(name__icontains=search_term).order_by(Lower('name'))

    else: # from is not filled in or first time the user sees page
        search_form = SearchForm()
        videos = Video.objects.order_by(Lower('name'))

    return render(request, 'video_collection/video_list.html',{'videos': videos, 'search_form': search_form})

