# defines url patterns for blogs

from django.urls import path

from . import views

app_name = 'blogs'

urlpatterns = [
    # home page
    path('', views.index, name='index'),
    # page that shows all blogs
    path('blogs/', views.blogs, name='blogs'),
    # detail posts for a single blog
    path('blogs/<int:blog_id>/', views.blog, name='blog'),
    # page for adding a new blog
    path('new_blog/', views.new_blog, name='new_blog'),
    # page for adding a new post
    path('new_post/<int:blog_id>/', views.new_post, name='new_post'),
    # page for editing an post
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),

]