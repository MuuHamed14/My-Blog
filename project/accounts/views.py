from django.shortcuts import render, redirect
from .forms import SignUpForm, UserProfile, UserForm
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login
from .models import Profile


def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('accounts:profile')
        else:
            form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def profile(request):
    my_profile = Profile.objects.get(user=request.user)
    return render(request, 'accounts/profile.html', {'my_profile': my_profile})


def edit_profile(request):
    my_profile = Profile.objects.get(user=request.user)
    user_form = UserForm(instance=request.user)
    user_profile = UserProfile(instance=my_profile)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        user_profile = UserProfile(request.POST, request.FILES, instance=my_profile)
        if user_form.is_valid() and user_profile.is_valid():
            user_form.save()
            user_profile1 = user_profile.save(commit=False)
            user_profile1.user = request.user
            user_profile1.save()
            return redirect(reverse('accounts:profile'))
        else:
            user_form = UserForm(request.POST, instance=request.user)
            user_profile = UserProfile(request.POST,instance=my_profile)
    return render(request,'accounts/edit_profile.html',{'user_form':user_form,'user_profile':user_profile})

