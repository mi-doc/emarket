from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from .forms import UserLoginForm, UserRegisterForm, EditProfileForm
from .models import Profile


def login_view(request):
    title = "Login"
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect("/")
    return render(request, "accounts/form.html", {"form":form, "title": title})


def register_view(request):
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)

        return redirect(reverse("accounts:edit-profile"))

    context = {
        "form": form,
        "title": title
    }
    return render(request, "accounts/form.html", context)


def logout_view(request):
    logout(request)
    return redirect("/")


@login_required(login_url='/accounts/login/')
def edit_profile_view(request):
    user = request.user
    title = "Edit profile"
    profile = Profile.objects.filter(user=user).first()

    if profile:
        form = EditProfileForm(instance=profile)
    else:
        form = EditProfileForm(request.POST or None)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect(reverse("accounts:profile"))

    context = {
        "form": form,
        "title": title
    }
    return render(request, "accounts/form.html", context)


@login_required(login_url='/accounts/login/')
def profile_view(request):
    user = request.user
    profile = Profile.objects.filter(user=user).first()

    return render(request, "accounts/profile.html", locals())
