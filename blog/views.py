from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Question
from .forms import PostForm
from django.utils import timezone


# Create your views here.
def post_list(request):
    posts = Post.objects.order_by('-created')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_new.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_new.html', {'form': form})


def polls(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    return render(request, 'blog/polls/polls.html', {'questions': latest_question_list})


def detail_polls(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'blog/polls/detail.html', {'question': question})
