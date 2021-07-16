from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, LikeView, bloglist

urlpatterns = [
    path('', PostListView, name='blog-home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('type/<str:type>/', views.TypePostListView, name='type-posts'),
    path('blog/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('blog/new/', PostCreateView, name='post-create'),
    path('blog/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('blog/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('like/<int:pk>', LikeView, name='post-like'),
    path('about/', views.about, name='blog-about'),
    path('api/<int:pk>/', views.blog_detail),
    path('api/update/<int:pk>/', views.blog_update),
    path('api/create', views.blog_create),
    path('api/<int:pk>/delete', views.blog_delete),
    path('api/list/', bloglist.as_view()),
]
