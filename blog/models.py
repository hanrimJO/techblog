from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'categories'


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = MarkdownxField()
    thumbnail_image = models.ImageField(upload_to='blog/%Y/%m/%d', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/{self.pk}/'

    def get_delete_url(self):
        return f'/{self.pk}/delete/'

    def get_update_url(self):
        return f'/{self.pk}/update/'

    def get_markdown_content(self):
        return markdown(self.content)

    class Meta:
        ordering = ['-created']



