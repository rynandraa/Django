from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from blog.models import Post


# Create your views here.

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account was created for: {username}!")
            return redirect('login')
        
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form":form})

@login_required
def profile(request):
    user_posts = Post.objects.filter(author=request.user)
    return render(request, "users/profile.html", {'posts' : user_posts})
