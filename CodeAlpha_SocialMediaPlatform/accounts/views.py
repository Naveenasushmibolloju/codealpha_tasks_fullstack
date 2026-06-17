from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from posts.models import Post
def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return redirect('/register/')

        if User.objects.filter(username=username).exists():
            return redirect('/register/')

        User.objects.create_user(username=username, password=password1)
        return redirect('/login/')

    return render(request, 'accounts/register.html')
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/login/')

    return render(request, 'accounts/login.html')
def logout_view(request):
    logout(request)
    return redirect('/login/')
def profile_view(request, username):
    user = get_object_or_404(User, username=username)

    profile = Profile.objects.get(user=user)

    posts = Post.objects.filter(
        user=user
    ).order_by('-created_at')

    return render(
        request,
        'accounts/profile.html',
        {
            'profile_user': user,
            'profile': profile,
            'posts': posts
        }
    )
def follow_unfollow(request, username):
    target_user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=target_user)

    if request.user in profile.followers.all():
        profile.followers.remove(request.user)
    else:
        profile.followers.add(request.user)

    return redirect('/profile/' + username)
@login_required
def edit_profile(request):

    
  
    profile, created = Profile.objects.get_or_create(
    user=request.user
)

    if request.method == "POST":

        profile.bio = request.POST.get("bio")

        if 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES['profile_pic']

        profile.save()

        return redirect(
            f'/profile/{request.user.username}/'
        )

    return render(
        request,
        'accounts/edit_profile.html',
        {'profile': profile}
    )