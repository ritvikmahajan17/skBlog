from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import post, TYPES
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PostCreateForm
from django.contrib import messages

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from blog.serializers import PostSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter


def LikeView(request, pk):
    if(request.user.is_anonymous):
        return HttpResponseRedirect(reverse('register'))

    post_likes = get_object_or_404(post, pk=pk)
    post_likes.likes.add(request.user)

    return HttpResponseRedirect(reverse('blog-home'))


class PostListView(ListView):
    model = post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-date_posted']


class UserPostListView(ListView):
    model = post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return post.objects.filter(author=user).order_by('-date_posted')


def PostListView(request):
    posts = post.objects.all().order_by('-date_posted')
    p_types = []
    for pType in TYPES:
        p_types.append(pType[0])

    context = {
        'posts': posts,
        'p_types': p_types
    }
    return render(request, 'blog/home.html', context=context)


def TypePostListView(request, type):
    posts = post.objects.filter(type=type).order_by('-date_posted')
    p_types = []
    for pType in TYPES:
        p_types.append(pType[0])

    context = {
        'posts': posts,
        'p_types': p_types
    }
    return render(request, 'blog/home.html', context=context)


class PostDetailView(DetailView):
    model = post
    context_object_name = 'post'


def PostCreateView(request):
    if request.method == 'POST':
        p_form = PostCreateForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = request.user
            instance.save()
            messages.success(request, f'Post Created!')
            return redirect('blog-home')
    else:
        p_form = PostCreateForm(instance=request.user.profile)

    context = {
        'form': p_form
    }
    return render(request, 'blog/post_form.html', context)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = post
    fields = ['title', 'type', 'img', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse('blog-home')


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = post

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse('blog-home')


def about(request):
    return render(request, 'blog/about.html')


## api views ##

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def blog_detail(request, pk):

    try:
        blog_post = post.objects.get(pk=pk)

    except post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(blog_post)
        return Response(serializer.data)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def blog_update(request, pk):

    try:
        blog_post = post.objects.get(pk=pk)

    except post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user

    if blog_post.author != user:
        return Response({'response': 'You are not allowed to edit this!'})

    if request.method == 'PUT':
        serializer = PostSerializer(blog_post, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = 'update successful'
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def blog_create(request):

    account = request.user
    blog_post = post(author=account)

    if request.method == 'POST':
        serializer = PostSerializer(blog_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def blog_delete(request, pk):

    try:
        blog_post = post.objects.get(pk=pk)

    except post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user

    if blog_post.author != user:
        return Response({'response': 'You are not allowed to delete this!'})

    if request.method == 'DELETE':
        operation = blog_post.delete()
        data = {}
        if operation:
            data["success"] = 'delete successful'
            return Response(data=data)

        return Response(status=status.HTTP_204_NO_CONTENT)


class bloglist(ListAPIView):
    queryset = post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ['title', 'content', 'author__username']
