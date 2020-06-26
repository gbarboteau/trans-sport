from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import SignUpForm, ConnexionForm, UpdateProfile
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

def index(request):
    template = loader.get_template('application/index.html')
    context = {}
    return HttpResponse(template.render(context,request=request))

def login_view(request):
    """Displays the account view and the user login form"""
    context = {}
    state = ""
    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            # gender = form.cleaned_data["gender"]
            # situation = form.cleaned_data["situation"]
            user = authenticate(username=username, password=password)  
            if user:
                login(request, user) 
            else: 
                state = "Votre username ou mot de passe est incorrect."
        else: 
            print(form.errors)
    else:
        form = ConnexionForm()
    template = loader.get_template('application/login.html')
    context = {'form': form, 'state': state}
    return HttpResponse(template.render(context, request=request))

def logout_view(request):
    """Log out the user and redirect the user to
    the index view
    """
    logout(request)
    return redirect('index')

@login_required
def account(request):
    my_user = request.user
    template = loader.get_template('application/account.html')
    context = {'user': my_user}
    return HttpResponse(template.render(context,request=request))

@login_required
def modify_account(request):
    my_user = request.user
    template = loader.get_template('application/modify-account.html')
    context = {'user': my_user}
    if request.method == 'POST':
        form = UpdateProfile(request.POST, initial={'username': my_user.username, 'email': my_user.email, 'gender': my_user.gender, 'situation': my_user.situation}, instance=my_user)
        form.actual_user = my_user
        if form.is_valid():
            form.save()
            template = loader.get_template('application/index.html')
            return HttpResponse(template.render(context, request=request))
        else:
            print(form.errors)
    else:
        form = UpdateProfile(initial={'username': my_user.username, 'email': my_user.email, 'gender': my_user.gender, 'situation': my_user.situation}, instance=my_user)
    context = {'user': my_user, 'form': form, 'errors': form.errors}
    return HttpResponse(template.render(context,request=request))

def create_account(request):
    context = {}
    template = loader.get_template('application/create-account.html')
    if request.method == 'POST':
        form_sign_up = SignUpForm(request.POST)
        if form_sign_up.is_valid():
            form_sign_up.save()
            username = form_sign_up.cleaned_data.get('username')
            email = form_sign_up.cleaned_data.get('email')
            password = form_sign_up.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponse(template.render(context, request=request))
        else:
            print(form_sign_up.errors)
    else:
        form_sign_up = SignUpForm()
    context = {'form_sign_up': form_sign_up}
    return HttpResponse(template.render(context,request=request))
