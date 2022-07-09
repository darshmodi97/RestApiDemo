from django.urls import path
from article import views

urlpatterns = [
    path('', views.ShowArticles.as_view(), name='show_articles'),
    path('detail/<pk>/', views.ArticleDetail.as_view(), name='article-detail'),
    path('create/', views.CreateArticleView.as_view(), name='create-article'),
    path('update/<pk>', views.UpdateArticleView.as_view(), name='update-article'),
    path('delete/<pk>', views.DeleteArticleView.as_view(), name='delete-article'),
]
