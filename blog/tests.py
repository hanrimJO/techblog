from django.test import TestCase, Client
from bs4 import BeautifulSoup
from blog.models import Post, Category
from django.contrib.auth.models import User
from django.utils import timezone


def create_post(title, content, author, created, modified, category=None):
    post_000 = Post.objects.create(
        title=title,
        content=content,
        author=author,
        created=timezone.now(),
        modified=timezone.now(),
        category=category
    )
    return post_000


def create_category(name='django', description=''):
     category, is_created = Category.objects.get_or_create(
         name=name,
         description=description
     )
     category.slug = category.name.replace(' ', '').replace('/', '')
     category.save()
     return category

class TestModel(TestCase):
    def setUp(self):
        self.client = Client()
        self.author_000 = User.objects.create(username='hanrim', password='nopassword')

    def test_category(self):
        category = create_category()

        post_000 = create_post(
            title='the first post',
            content='Hello World',
            author=self.author_000,
            created=timezone.now(),
            modified=timezone.now(),
            category=category
        )
        self.assertEqual(category.post_set.count(), 1)

    def test_post(self):
        category = create_category()
        post_000 = create_post(
            title='the first post',
            content='Hello World',
            author=self.author_000,
            created=timezone.now(),
            modified=timezone.now(),
            category=category
        )


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.author_000 = User.objects.create_user(username='hanrim', password='nopassword')

    def test_post_list_no_post(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        main_div = soup.find('div', id='main-div')

        self.assertIn('게시물이 아직 없습니다', main_div.text)

    def test_post_list_post(self):
        post_000 = create_post(
            title='the first post',
            content='Hello World',
            author=self.author_000,
            created=timezone.now(),
            modified=timezone.now(),
        )
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        main_div = soup.find('div', id='main-div')

        self.assertNotIn('게시물이 아직 없습니다', main_div.text)
        self.assertIn(post_000.title, main_div.text)
        self.assertEqual(Post.objects.all().count(), 1)

    def test_post_list_without_category(self):
        post_000 = create_post(
            title='the first post',
            content='Hello World',
            author=self.author_000,
            created=timezone.now(),
            modified=timezone.now(),
        )
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        category_div = soup.find('div', id='side-div')

        self.assertNotIn('django', category_div.text)
        self.assertIn('기타', category_div.text)




    def test_post_create(self):
        category = create_category()
        post_000 = create_post(
            title='the first post',
            content='Hello World',
            author=self.author_000,
            created=timezone.now(),
            modified=timezone.now(),
            category=category
        )
        self.assertEqual(Post.objects.all().count(), 1)


    def test_post_update(self):
        category = create_category()
        time_now = timezone.now()
        post_000 = create_post(
            title='the first post',
            content='Hello World',
            author=self.author_000,
            created=time_now,
            modified=time_now,
            category=category
        )
        print(post_000.created, post_000.modified)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual('the first post', post_000.title)

        post_000.title = 'hihihi'
        post_000.save()

        print(post_000.created, post_000.modified)
        self.assertEqual('hihihi', post_000.title)







