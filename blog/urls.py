from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('<int:pk>/update/', views.PostUpdate.as_view()),
    path('category/<str:slug>/', views.PostListCategory.as_view()),
    path('create/', views.PostCreate.as_view()),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout')
]
