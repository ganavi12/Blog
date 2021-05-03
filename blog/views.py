from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404
from django.template.loader import render_to_string
# from datetime import date
from .models import Post,Tag,Author

# all_posts = []


# def get_date(post):
#     return post['date']

def starting_page(request):
    # render(request, "blog/index.html")
    # return HttpResponse("hi")\
    latest_posts = Post.objects.all().order_by("-date")[:3]
    # sorted_posts = sorted(all_posts,key=get_date)
    # latest_posts = sorted_posts[-3:]
    # render(request, "blog/index.html",{"posts":latest_posts})
    msg = render_to_string("blog/index.html",{"posts":latest_posts})
    return HttpResponse(msg)

 
def posts(request):
    try:
        # render(request, "blog/all-posts.html")
        all_posts = Post.objects.all().order_by("-date") 
        msg = render_to_string("blog/all-posts.html",{"all_posts":all_posts}) 
        return HttpResponse(msg)
    except:
        raise Http404("404.html") 

def post_details(request,slug): 
    # identifeid_post = next(post for post in all_posts if post['slug'] ==slug)
    # identifeid_post = Post.objects.get(slug=slug)
    identifeid_post = get_object_or_404(Post,slug=slug)
    msg = render_to_string("blog/post-detail.html",{"post":identifeid_post,"post_tags":identifeid_post.tags.all()})  
    return HttpResponse(msg)
# Create your views here.


def getdata(request):
    identifeid_post = Post.objects.get(title='Programming Is Great!')
    final = identifeid_post.tags.all()
    final1 = identifeid_post.author.email_address
    return HttpResponse(final1)
