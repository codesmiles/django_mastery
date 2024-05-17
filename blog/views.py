from django.shortcuts import render
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    DeleteView,
    UpdateView
    )
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.
from django.contrib.auth.decorators import login_required

# @login_required
# def home(request):
#     context = {
#         'posts': Post.objects.all(),
#     }
#     return render(request, 'blog/pages/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/pages/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/pages/post_detail.html'
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/pages/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/pages/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self) -> bool | None:
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Post
    template_name = 'blog/pages/post_confirm_delete.html'
    success_url = 'blog/'
    
    def test_func(self) -> bool | None:
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    

@login_required
def about(request):
    return render(request, 'blog/pages/about.html',{"title": "About"})