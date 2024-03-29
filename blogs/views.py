from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Blog, Post
from .forms import BlogForm, PostForm


# Create your views here.



def index(request):
    # the home page for Blog
    return render(request, 'blogs/index.xhtml')

@login_required
def blogs(request):
    # show all blogs
    blogs = Blog.objects.filter(owner=request.user).order_by('date_added')
    context = {'blogs': blogs}
    return render(request, 'blogs/blogs.xhtml', context)

@login_required
def blog(request, blog_id):
    # show a single blog and all it's posts
    blog = Blog.objects.get(id=blog_id)

    posts = blog.post_set.order_by('-date_added')

    context = {'blog': blog, 'posts': posts}

    return render(request, 'blogs/blog.xhtml', context)


@login_required
def new_blog(request):
    # add a new blog
    if request.method != 'POST':
        # no data submitted, create a blank form
        form = BlogForm()
    else:
        # POST data submitted; process data
        form = BlogForm(data=request.POST)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.owner = request.user
            new_blog.save()
            return redirect('blogs:blogs')
    
    # display a blank or invalid form
    context = {'form': form}
    return render(request, 'blogs/new_blog.xhtml', context)

@login_required
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
            check_blog_owner(blog, request)
            new_post.save()
            return redirect('blogs:blog', blog_id=blog_id)
    # display a blank or invalid form
    context = {'blog': blog, 'form': form}
    return render(request,'blogs/new_post.xhtml', context)

@login_required
def edit_post(request, post_id):
    # edit an existing post
    post = Post.objects.get(id=post_id)
    blog = post.blog
    check_blog_owner(blog, request)

    if request.method != 'POST':
        # inital requestl pre-fill form with the current entry
        form = PostForm(instance=post)
    else:
        # POST data submitted ; process data
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:blog', blog_id=blog.id)
        
    context = {'post': post, 'blog': blog, 'form' : form}
    return render(request, 'blogs/edit_post.xhtml', context)

#code to check owner belongs to current user
def check_blog_owner(blog, request):
    if blog.owner != request.user:
        raise Http404
