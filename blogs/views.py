from django.shortcuts import render
from .models import Blog
# Create your views here.

def index(request):
    # the home page for Blog
    return render(request, 'blogs/index.xhtml')

def blogs(request):
    # show all blogs
    blogs = Blog.objects.order_by('date_added')
    context = {'blogs': blogs}
    return render(request, 'blogs/blogs.xhtml', context)

def blog(request, blog_id):
    # show a single blog and all it's posts
    blog = Blog.objects.get(id=blog_id)

    posts = blog.post_set.order_by('-date_added')

    context = {'blog': blog, 'posts': posts}

    return render(request, 'blogs/blog.xhtml', context)

