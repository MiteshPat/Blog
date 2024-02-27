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

