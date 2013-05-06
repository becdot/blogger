from django import forms
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

from django.contrib.auth.models import User
from blog.models import Post


class NewPost(forms.Form):
    title = forms.CharField(max_length=200)
    content = forms.CharField(widget=forms.Textarea)
    error_css_class = 'error'

    def create_new_blog_post(self, user):
        user.post_set.create(
            author='user.username',
            date=timezone.now(),
            title=self.cleaned_data['title'],
            content=self.cleaned_data['content'])


def signup(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return redirect('blog.views.welcome')
        else:
            return render(request, 'signup.html', {'error':None}) 
    else:
        submit_user = request.POST['username']
        submit_pw = request.POST['password']
        try:
            user = User.objects.get(username=submit_user)
            return render(request, 'signup.html', {'error':'That username is already taken.'})
        except User.DoesNotExist:
            user = User.objects.create_user(submit_user, password=submit_pw)
            user = authenticate(username=submit_user, password=submit_pw)
            if user:
                login(request, user)
                return redirect('blog.views.welcome')

def login_user(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return redirect('blog.views.welcome')
        else:
            return render(request, 'login.html', {'error':None})
    else:
        submit_user = request.POST['username']
        submit_pw = request.POST['password']
        user = authenticate(username=submit_user, password=submit_pw)
        if user:
            login(request, user)
            return redirect('/welcome')
        else:
            return render(request, 'login.html', {'error':'That username or password does not exist'})

def logout_user(request):
    logout(request)
    return redirect('/')

def welcome(request):
    if request.user.is_authenticated():
        return render(request, 'welcome.html', {'username':request.user.username})
    else:
        return redirect('blog.views.login_user')

def new_post(request):
    if request.user.is_authenticated():
        if request.method == 'GET':
            new = NewPost()
        else:
            new = NewPost(request.POST)
            if new.is_valid():
                new.create_new_blog_post(request.user)
                return redirect('/view/recent/10')
        return render(request, 'new_post.html', {'form':new})
    else:
        return redirect('blog.views.login_user')

def view_recent(request, more):
    more = int(more)
    posts = Post.objects.filter(author=request.user).order_by('-date')[:more]
    if len(posts) < more:
        return render(request, 'view_all.html', {'posts':posts, 'more': False})
    return render(request, 'view_all.html', {'posts':posts, 'more': more + 10})

def view_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    next = Post.objects.filter(author=post.author, date__gt=post.date) 
    next = next[0] if next else None
    prev = Post.objects.filter(author=post.author, date__lt=post.date).order_by('-date')
    prev = prev[0] if prev else None
    return render(request, 'view_one.html', {'post':post, 'next':next, 'prev':prev})


