from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DeleteView
from taggit.models import Tag

from blog.forms import CommentForm
from blog.models import Post, Comment


@login_required
def main(request, tag_slug=None):
    tags = Tag.objects.all()
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # 9 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/posts.html', {'page': page, 'posts': posts, 'tag': tag, 'tags': tags})


@login_required
def post_detail(request, post):
    post = get_object_or_404(Post, slug=post, status='published')

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Assign the comment to the user
            new_comment.user = request.user
            # Save the comment to the database
            new_comment.save()

    comment_form = CommentForm()
    return render(request, 'blog/detail.html',
                  {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})


@login_required
def post_like(request, post):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if request.user in post.users_like.all():
        post.users_like.remove(request.user)
    else:
        post.users_like.add(request.user)
    return HttpResponseRedirect(reverse('blog:post_detail', args=(post,)))


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.has_perm('blog.delete_comment') or (request.user == comment.user):
        if request.method == "POST":
            comment.delete()
            return HttpResponseRedirect(reverse('blog:post_detail', args=(comment.post.slug,)))

        return render(request, 'blog/comment_confirm_delete.html')
    else:
        raise PermissionError
