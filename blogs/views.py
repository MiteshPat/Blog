from django.shortcuts import render, redirect
from .models import Blog
from .forms import BlogForm, PostForm
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

def new_blog(request):
    # add a new blog
    if request.method != 'POST':
        # no data submitted, create a blank form
        form = BlogForm()
    else:
        # POST data submitted; process data
        form = BlogForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:blogs')
    
    # display a blank or invalid form
    context = {'form': form}
    return render(request, 'blogs/new_blog.xhtml', context)

def new_post(request, blog_id):
    # add a new post for a particular blog
    blog = Blog.objects.get(id=blog_id)

    if request.method != 'POST':
        # no data submitted; create a blank form
        form = PostForm()
    else:
        # POST data submitted; process data
        form = PostForm(data=request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.blog = blog
            new_post.save()
            return redirect('blogs:blog', blog_id=blog_id)
    # display a blank or invalid form
    context = {'blog': blog, 'form': form}
    return render(request,'blogs/new_post.xhtml', context)