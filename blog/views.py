from django.shortcuts import render, redirect
from blog.models import Post, Category
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
# Create your views here.

class PostList(ListView):
    model = Post
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()
        return context


class PostDetail(DetailView):
    model = Post


class PostListCategory(ListView):
    def get_queryset(self):
        slug = self.kwargs['slug']
        if slug == '_none':
            category = None
        else:
            category = Category.objects.get(slug=slug)
        return Post.objects.filter(category=category).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostListCategory, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()

        slug = self.kwargs['slug']
        if slug == '_none':
            context['category'] = '기타'
        else:
            category = Category.objects.get(slug=slug)
            context['category'] = category
        return context




