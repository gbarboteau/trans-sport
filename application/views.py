from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import User, Category, Adress, Place, Comment
from .forms import SignUpForm, ConnexionForm, UpdateProfile, PlaceSubmissionForm, CommentForm, SearchForm
from .utils import GetCityDepartementAndRegion, DoesKeyExists, GetNote
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from .tokens import account_activation_token
import random

User = get_user_model()

def index(request):
    all_places = Place.objects.all()
    random_places = random.sample(list(all_places), 2)
    template = loader.get_template('application/index.html')
    context = {'random_places': random_places}
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

# def create_account(request):
#     context = {}
#     template = loader.get_template('application/create-account.html')
#     if request.method == 'POST':
#         form_sign_up = SignUpForm(request.POST)
#         if form_sign_up.is_valid():
#             form_sign_up.save()
#             username = form_sign_up.cleaned_data.get('username')
#             email = form_sign_up.cleaned_data.get('email')
#             password = form_sign_up.cleaned_data.get('password1')
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             return HttpResponse(template.render(context, request=request))
#         else:
#             print(form_sign_up.errors)
#     else:
#         form_sign_up = SignUpForm()
#     context = {'form_sign_up': form_sign_up}
#     return HttpResponse(template.render(context,request=request))

class create_account(View):
    form_class = SignUpForm
    template = 'application/create-account.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            print("form valide")
            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('application/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # print("uid : " + str(message.uid) + "\n token : " + str(message.token))
            user.email_user(subject, message)

            messages.success(request, ('Please Confirm your email to complete registration.'))
            print("engregistré")
            return redirect('index')

        return render(request, self.template, {'form': form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('index')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('index')


@login_required
def suggesting_new_place(request):
    my_user = request.user
    template = loader.get_template('application/suggesting-new-place.html')
    context = {'user': my_user}
    if request.method == 'POST':
        form = PlaceSubmissionForm(request.POST)
        if form.is_valid():
            try:
                """Creating a new adress"""
                my_departement_and_region = GetCityDepartementAndRegion(form.data['postal_code'])
                new_adress = Adress(postal_code=form.data['postal_code'], street_adress=form.data['street_adress'], departement=my_departement_and_region[1], region=my_departement_and_region[2], city=my_departement_and_region[0]) 
                new_adress.save()
                """Creating a new place"""
                new_place = Place(name=form.data['name'], picture=form.data['picture'], description=form.data['description'], website=form.data['website'], contact_mail=form.data['contact_mail'], contact_phone=form.data['contact_phone'], can_be_seen=False, adress_id=new_adress.id, category_id=form.data['category'])
                new_place.save()
                """Creating a new comment"""
                new_comment = Comment(comment=form.data['comment'], score_global=form.data['score_global'], can_you_enter=DoesKeyExists('can_you_enter', form.data), are_you_safe_enough=DoesKeyExists('are_you_safe_enough', form.data), is_mixed_lockers=DoesKeyExists('is_mixed_lockers', form.data), is_inclusive_lockers=DoesKeyExists('is_inclusive_lockers', form.data), has_respectful_staff=DoesKeyExists('has_respectful_staff', form.data), place_id=new_place.id, user_id=my_user.id)
                print(form.data['comment'])
                print(new_comment.comment)
                new_comment.save()

                context = {'is_added': True}
            except IntegrityError as error:
                context = {'is_added': False}
            template = loader.get_template('application/index.html')
            return HttpResponse(template.render(context, request=request))
        else:
            print(form.errors)
    else:
        form = PlaceSubmissionForm()
    context = {'user': my_user, 'form': form, 'errors': form.errors}
    return HttpResponse(template.render(context,request=request))

def search_places(request):
    query = request.GET.get('query')
    page = request.GET.get('page')
    queryset = Place.objects.filter(name__icontains=query, can_be_seen=True) | Place.objects.filter(adress__street_adress__icontains=query, can_be_seen=True) | Place.objects.filter(adress__region__icontains=query, can_be_seen=True) | Place.objects.filter(adress__departement__icontains=query, can_be_seen=True) | Place.objects.filter(adress__postal_code__icontains=query, can_be_seen=True) | Place.objects.filter(adress__city__icontains=query, can_be_seen=True)
    paginator = Paginator(queryset, 9)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    title = "Résultats pour la requête %s"%query
    context = {'queryset': queryset, 'paginate': True, 'query': query}
    template = loader.get_template('application/search.html')
    return HttpResponse(template.render(context, request=request))


def all_places(request):
    places = Place.objects.all()
    print(places)
    context = {'places': places}
    template = loader.get_template('application/all-places.html')
    return HttpResponse(template.render(context, request=request))

def show_place(request, place_id):
    print("path is good")
    this_place = get_object_or_404(Place, pk=place_id, can_be_seen=True)
    its_comments = Comment.objects.filter(place_id=this_place.id)
    this_place.note_global = GetNote(its_comments.filter(score_global='P').count(), its_comments.filter(score_global='N').count())
    this_place.note_can_you_enter = GetNote(its_comments.filter(can_you_enter=True).count(), its_comments.filter(can_you_enter =False).count())
    this_place.note_are_you_safe_enough = GetNote(its_comments.filter(are_you_safe_enough=True).count(), its_comments.filter(are_you_safe_enough =False).count())
    this_place.note_is_mixed_lockers = GetNote(its_comments.filter(is_mixed_lockers=True).count(), its_comments.filter(is_mixed_lockers =False).count())
    this_place.note_is_inclusive_lockers = GetNote(its_comments.filter(is_inclusive_lockers=True).count(), its_comments.filter(is_inclusive_lockers =False).count())
    this_place.note_has_respectful_staff = GetNote(its_comments.filter(has_respectful_staff=True).count(), its_comments.filter(has_respectful_staff =False).count())
    template = loader.get_template('application/show-place.html')
    does_comment_exists = False
    for comment in its_comments:
        if comment.user == request.user:
            does_comment_exists = True
    print("does comment exists : " + str(does_comment_exists))
    context = {'this_place': this_place, 'its_comments': its_comments, 'does_comment_exists': does_comment_exists, 'place_id': place_id}
    return HttpResponse(template.render(context,request=request))

@login_required
def edit_comment(request, place_id):
    my_user = request.user
    template = loader.get_template('application/edit-comment.html')
    context = {'user': my_user}
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            try:
                edited_comment = get_object_or_404(Comment, place_id=place_id, user_id=my_user.id)
                edited_comment.comment = form.data['comment']
                edited_comment.score_global = form.data['score_global']
                edited_comment.can_you_enter = DoesKeyExists('can_you_enter', form.data)
                edited_comment.are_you_safe_enough = DoesKeyExists('are_you_safe_enough', form.data)
                edited_comment.is_mixed_lockers = DoesKeyExists('is_mixed_lockers', form.data)
                edited_comment.is_inclusive_lockers = DoesKeyExists('is_inclusive_lockers', form.data)
                edited_comment.has_respectful_staff = DoesKeyExists('has_respectful_staff', form.data)
                edited_comment.save()
                context = {'is_added': True}
            except IntegrityError as error:
                context = {'is_added': False}
            return HttpResponse(template.render(context, request=request))
        else:
            print(form.errors)
    else:
        form = CommentForm()
    context = {'user': my_user, 'form': form, 'errors': form.errors}
    return HttpResponse(template.render(context,request=request))

@login_required
def make_comment(request, place_id):
    my_user = request.user
    template = loader.get_template('application/make-comment.html')
    context = {'user': my_user}
    if request.method == 'POST':
        form = CommentForm(request.POST)
        # form.actual_user = my_user
        if form.is_valid():

            try:
                new_comment = Comment(comment=form.data['comment'], score_global=form.data['score_global'], can_you_enter=DoesKeyExists('can_you_enter', form.data), are_you_safe_enough=DoesKeyExists('are_you_safe_enough', form.data), is_mixed_lockers=DoesKeyExists('is_mixed_lockers', form.data), is_inclusive_lockers=DoesKeyExists('is_inclusive_lockers', form.data), has_respectful_staff=DoesKeyExists('has_respectful_staff', form.data), place_id=place_id, user_id=my_user.id)
                print(form.data['comment'])
                print(new_comment.comment)
                new_comment.save()
                context = {'is_added': True}
            except IntegrityError as error:
                context = {'is_added': False}
            return HttpResponse(template.render(context, request=request))
        else:
            print(form.errors)
    else:
        form = CommentForm()
    context = {'user': my_user, 'form': form, 'errors': form.errors}
    return HttpResponse(template.render(context,request=request))
