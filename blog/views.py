from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template.loader import render_to_string
# from datetime import date
from .models import Post, Tag, Author
from django.views.generic import ListView, DetailView
from .forms import CommentForm
from django.views import View
from django.urls import reverse

# all_posts = []


# def get_date(post):
#     return post['date']

# def starting_page(request):
#     # render(request, "blog/index.html")
#     # return HttpResponse("hi")\
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     # sorted_posts = sorted(all_posts,key=get_date)
#     # latest_posts = sorted_posts[-3:]
#     # render(request, "blog/index.html",{"posts":latest_posts})
#     msg = render_to_string("blog/index.html",{"posts":latest_posts})
#     return HttpResponse(msg)


class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        querset = super().get_queryset()
        data = querset[:3]
        return data
    

 
# def posts(request):
#     try:
#         # render(request, "blog/all-posts.html")
#         all_posts = Post.objects.all().order_by("-date") 
#         msg = render_to_string("blog/all-posts.html",{"all_posts":all_posts}) 
#         return HttpResponse(msg)
#     except:
#         raise Http404("404.html")

class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"
    

# def post_details(request,slug): 
#     # identifeid_post = next(post for post in all_posts if post['slug'] ==slug)
#     # identifeid_post = Post.objects.get(slug=slug)
#     identifeid_post = get_object_or_404(Post,slug=slug)
#     msg = render_to_string("blog/post-detail.html",{"post":identifeid_post,"post_tags":identifeid_post.tags.all()})  
#     return HttpResponse(msg)


# class SinglePostView(DetailView):
#     template_name = "blog/post-detail.html"
#     model = Post
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["post_tags"] = self.object.tags.all()
#         context["comment_form"] = CommentForm()
#         return context


class SinglePostView(View):
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
          is_saved_for_later = post_id in stored_posts
        else:
          is_saved_for_later = False
        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all(),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request,"blog/post-detail.html",context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-details-page", args=[slug]))
            
       
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all(),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)
        
class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context = {}
        if stored_posts is None or len(stored_posts) == 0:
            context['posts'] = []
            context['has_posts'] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context['posts'] = posts
            context['has_posts'] = True 
        return render(request,"blog/stored-posts.html",context)

    def post(self, request):
        post_id = int(request.POST['post.id'])
        stored_posts = request.session.get("stored_posts")
        if stored_posts is None:
            stored_posts = []
        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
        request.session["stored_posts"] = stored_posts
        return HttpResponseRedirect("/") 
      