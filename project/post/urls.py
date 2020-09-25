from django.urls import path
from . import views

app_name = 'post'
urlpatterns = [

    # Function Based View
    path('all_posts/', views.all_posts, name='all_posts'),
    path('post/<int:id>/', views.one_post, name='post'),
    path('create_post/', views.create_post, name='create_post'),
    path('<int:id>/edit/', views.edit_post, name='edit_post'),

    # Class Based View
    path('all_posts1/',views.PostList.as_view(),name='all_posts1'),
    path('all_posts1/<int:id>/',views.PostDetail.as_view(),name='all_posts1_detail'),
    path('post_create/', views.PostCreate.as_view(), name='post_create'),
    path('post_update/<int:id>/', views.PostUpdate.as_view(), name='post_update'),

]
