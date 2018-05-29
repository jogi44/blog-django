from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.utils import timezone
from .models import Post, Comment
from django.template import RequestContext
from django.http import *
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.http import HttpResponseRedirect


def base(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:3]
    return render(request, 'blog/base.html', {'posts': posts})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post.html', {'post': post})


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post', pk=comment.post.pk)
    #return redirect(request, 'post', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post', pk=comment.post.pk)
    #return redirect(request, 'post', pk=comment.post.pk)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('base')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
