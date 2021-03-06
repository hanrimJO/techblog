from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('<int:pk>/update/', views.PostUpdate.as_view()),
    path('<int:pk>/delete/', views.PostDelete.as_view()),
    path('category/<str:slug>/', views.PostListCategory.as_view()),
    path('create/', views.PostCreate.as_view()),
    path('create-category/', views.PostCreateCategory.as_view()),
    path('search/<str:q>/', views.PostSearch.as_view()),
    path('about_me/', views.about_me),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout')
]
