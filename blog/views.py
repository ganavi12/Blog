from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.template.loader import render_to_string
from datetime import date

all_posts = [
    { 
        "slug": "hike-in-the-mountains",
        "image": "mountain.jpg",
        "author": "Ganavi",
        "date": date(2021, 7, 12),
        "title": "Mountain Hiking",
        "excerpt": "There's nothing like the views you get when hiking in the mountains! And I wasn't even prepared for what happened whilst I was enjoying the view!",
        "content": """
         A mountain is an elevated portion of the Earth's crust, generally with steep sides that show
          significant exposed bedrock. A mountain differs from a plateau in having a limited summit area, 
          and is larger than a hill, typically rising at least 300 metres (1000 feet) above the surrounding land
        """
    },
    {
        "slug": "programming-is-fun",
        "image": "coding.jpg",
        "author": "Ganavi",
        "date": date(2021, 8, 10),
        "title": "Programming Is Great!",
        "excerpt": "Did you ever spend hours searching that one error in your code? Yep - that's what happened to me yesterday...",
        "content": """
          Coding is a list of step-by-step instructions that get computers to do what you want them to do.
           Coding makes it possible for us to create computer software, games, apps and websites. Coders,
            or programmers, are people who write the programmes behind everything we see and do on a computer
        """
    },
    {
        "slug": "into-the-woods",
        "image": "woods.jpg",
        "author": "Ganavi",
        "date": date(2021, 10, 5),
        "title": "Nature At Its Best",
        "excerpt": "Nature is amazing! The amount of inspiration I get when walking in nature is incredible!",
        "content": """
         Wood is the main substance in trees. It is mainly formed by the xylem vessels which carry water up
          the plant. The two main substances in wood are cellulose and lignin. Wood is used to make buildings
           and furniture, and also for art.
        """
    }
]


def get_date(post):
    return post['date']

def starting_page(request):
    # render(request, "blog/index.html")
    # return HttpResponse("hi")\
    sorted_posts = sorted(all_posts,key=get_date)
    latest_posts = sorted_posts[-3:]
    # render(request, "blog/index.html",{"posts":latest_posts})
    msg = render_to_string("blog/index.html",{"posts":latest_posts})
    return HttpResponse(msg)

 
def posts(request):
    try:
        # render(request, "blog/all-posts.html")
        msg = render_to_string("blog/all-posts.html",{"all_posts":all_posts}) 
        return HttpResponse(msg)
    except:
        raise Http404("404.html")

def post_details(request,slug):
    identifeid_post = next(post for post in all_posts if post['slug'] ==slug)
    msg = render_to_string("blog/post-detail.html",{"post":identifeid_post}) 
    return HttpResponse(msg)
# Create your views here.
