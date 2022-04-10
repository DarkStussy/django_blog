from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.forms import UserRegistrationForm, UserForm


def login_user(request):
    error = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("blog:main")
        else:
            error = 'Login or password is incorrect'

    return render(request, 'accounts/login_user.html', {'error': error})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'accounts/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'user_form': user_form})


@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile has been saved successfully!')
        else:
            messages.error(request, 'Unable to complete request')
        return redirect("accounts:profile")
    user_form = UserForm(instance=request.user)
    return render(request=request, template_name="accounts/profile.html", context={"user_form": user_form})
