from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.views.generic import TemplateView, DetailView


class PostListView(TemplateView):
    template_name = "blog/post_list.html"

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(published_date__lte=timezone.now()).order_by("published_date")
        return context
# def post_list(request):
#     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
#         'published_date')
#     return render(request, 'blog/post_list.html', {'posts': posts})
#     # return render(request, 'blog/post_list.html')post_list


class PostDetailView(DetailView):

    model = Post

    # def get_context_data(self, **pk):
    #     print(pk)
    #     context = super(PostDetailView, self).get_context_data(pk)
    #     context["post"] = get_object_or_404(Post, pk=pk)
    #     return context

# class PostDetailView(TemplateView):
#     template_name = "blog/post_detail.html"
#
#     def get_context_data(self, pk):
#         context = super(PostDetailView, self).get_context_data(pk=pk)
#         context["post"] = get_object_or_404(Post, pk=pk)
#         return context

# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
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
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
