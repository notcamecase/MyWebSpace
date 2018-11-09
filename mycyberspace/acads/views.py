from django.shortcuts import render
from django.http import HttpResponse
from .models import Post,Image
import re
# Create your views here.

def home(request):
    return render(request, 'acads/post_list.html', {})

def show_all_post(request):
    post = Post.objects.order_by('-created_date')


    return render(request,'acads/all_posts.html',{'posts':post})

def single_post(request ,post_id):

    posts = Post.objects.order_by('-created_date')
    if not posts:
        return HttpResponse("<p>No Post Yet</p>")
    post = Post.objects.get(pk=post_id)
    if not post:
        return HttpResponse("<p>What you are searching is not on this server or deleted</p>")

    return render(request,'acads/single_post.html',{'post':post,'posts':posts})

def search(request):
    if 'searcher' in request.GET:
        search_param = request.GET['searcher']
    else:
        search_param = "E.m.p.t.y__S.t.r.i.n.g"

    posts = Post.objects.order_by('-created_date')
    required_post = []
    search_param = str(search_param)
    if not posts:
        return HttpResponse("<p>No Post Yet</p>")
    for post in posts:
        cleanr = re.compile('<.*?>')
        pt =  re.sub(cleanr,'',str(post.text)+' '+str(post.title)+' '+str(post.author))
        if search_param.upper() in pt.upper():
            required_post.append(post)
    return render(request,'acads/search_result.html', {'post':required_post,'posts':posts,'search_param':search_param})
