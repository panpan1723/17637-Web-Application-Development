from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from socialnetwork.forms import LoginForm, RegisterForm, EntryForm

# def login_action(request):
#     context = {}

#     if request.method == 'GET':
#         return render(request, 'login.html', context)

def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        if request.user.is_authenticated:
            context['post_text'] = "I waited in line for 15 minutes to get my lunch"
            context['post_author'] = "Jeff Eppinger"
            context['post_time'] = "8/25/2021 12:10 PM"
            context['comment_text'] = "Can we have BBQ?"
            context['comment_author'] = "James Garrett"
            context['comment_time'] = "8/25/2021 1:13 PM"
            return render(request, 'socialnetwork/global_stream.html', context)
        return render(request, 'socialnetwork/login.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('global_stream'))

# def register_action(request):
#     context = {}

#     if request.method == 'GET':
#         return render(request, 'socialnetwork/register.html', context)

def register_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'socialnetwork/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegisterForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('global_stream'))

@login_required
def global_stream_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['post_text'] = "I waited in line for 15 minutes to get my lunch"
        context['post_author'] = "Jeff Eppinger"
        context['post_time'] = "8/25/2021 12:10 PM"
        context['comment_text'] = "Can we have BBQ?"
        context['comment_author'] = "James Garrett"
        context['comment_time'] = "8/25/2021 1:13 PM"
        # context['first_name'] = request.POST['first_name']
        # context['last_name'] = request.POST['last_name']
        # if request.user.is_authenticated():
        #     first_name = request.user.first_name
        #     context['first_name'] = request.POST['first_name']
        
        return render(request, 'socialnetwork/global_stream.html', context)

    # new_post = _process_param(request.POST, "post_input_text")
    # all_posts = _process_param(request.POST, "all_posts")

@login_required
def follower_stream_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['post_text'] = "I waited in line for 15 minutes to get my lunch"
        context['post_author'] = "Jeff Eppinger"
        context['post_time'] = "8/25/2021 12:10 PM"
        context['comment_text'] = "Can we have BBQ?"
        context['comment_author'] = "James Garrett"
        context['comment_time'] = "8/25/2021 1:13 PM"
        
        return render(request, 'socialnetwork/follower_stream.html', context)

def _process_param(request_method, param):
    if param in request_method:
        text = request_method[param]
        return text

@login_required
def my_profile_action(request):
    context = {}

    if request.method == 'GET':
        return render(request, 'socialnetwork/my_profile.html', context)

@login_required
def other_profile_action(request):
    context = {}

    if request.method == 'GET':
        return render(request, 'socialnetwork/other_profile.html', context)

def logout_action(request):
    logout(request)
    return redirect(reverse('login'))