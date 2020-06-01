from django.shortcuts import render, redirect
from blog.models import Post, Category
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth.models import User
# Create your views here.


class PostList(ListView):
    model = Post
    paginate_by = 5
    form_class = AuthenticationForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()
        return context


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()
        return context


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

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return redirect('/')
    else:
        return redirect('/')

def logout(request):
    auth.logout(request)
    return redirect('/')