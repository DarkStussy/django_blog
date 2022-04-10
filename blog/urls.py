from django.urls import path
from .views import main, post_detail, post_like, delete_comment

app_name = 'blog'

urlpatterns = [
    path('', main, name='main'),
    path('<slug:post>/', post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>/', main, name='post_list_by_tag'),
    path('like/<slug:post>/', post_like, name='post-like'),
    path('<int:pk>/delete_comment/', delete_comment, name='delete-comment'),
]
