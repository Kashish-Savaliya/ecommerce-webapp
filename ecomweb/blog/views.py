from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
# Create your views here.


def index(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})


def blogpost(request, id):
    post = Post.objects.filter(post_id=id)[0]
    print(post)
    return render(request, 'blog/blogpost.html', {'post': post})
