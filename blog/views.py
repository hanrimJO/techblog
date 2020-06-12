from django.shortcuts import render, redirect
from blog.models import Post, Category
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import auth
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator
# Create your views here.


class PostList(ListView):
    model = Post
    paginate_by = 5
    form_class = AuthenticationForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        category_all = Category.objects.all()
        category_list = []
        for i in category_all:
            category_num = Post.objects.filter(category=i).count()
            if category_num != 0:
                category_list.append(i)
        context['category_list'] = category_list
        context['posts_without_category'] = Post.objects.filter(category=None).count()

        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)
        page = self.request.GET.get('page')
        current_page = int(page) if page else 1
        start_index = int((current_page - 1)/page_numbers_range)*page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        context['start'] = start_index
        context['end'] = max_index
        return context


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()

        return context


class PostListCategory(PostList):
    def get_queryset(self):
        slug = self.kwargs['slug']
        if slug == '_none':
            category = None
        else:
            category = Category.objects.get(slug=slug)
        return Post.objects.filter(category=category).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostListCategory, self).get_context_data(**kwargs)
        category_all = Category.objects.all()
        category_list = []
        for i in category_all:
            category_num = Post.objects.filter(category=i).count()
            if category_num != 0:
                category_list.append(i)
        context['category_list'] = category_list
        context['posts_without_category'] = Post.objects.filter(category=None).count()

        slug = self.kwargs['slug']
        if slug == '_none':
            context['category'] = '기타'
        else:
            category = Category.objects.get(slug=slug)
            context['category'] = category
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'thumbnail_image', 'category']
    login_url = '/login/'

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(type(self), self).form_valid(form)
        else:
            return redirect('/')


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'thumbnail_image', 'category']
    login_url = '/login/'


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    login_url = '/login/'
    success_url = '/'


class PostSearch(PostList):
    def get_queryset(self):
        q = self.kwargs['q']
        object_list = Post.objects.filter(Q(title__contains=q) | Q(content__contains=q))
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostSearch, self).get_context_data()
        context['search_info'] = f'Search: {self.kwargs["q"]}'
        q = self.kwargs['q']
        context['search_count'] = Post.objects.filter(Q(title__contains=q) | Q(content__contains=q)).count()
        return context


def login_view(request):
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


def logout_view(request):
    auth.logout(request)
    return redirect('/')


def about_me(request):
    return render(request, 'blog/about_me.html', {})