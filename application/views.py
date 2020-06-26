from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import User, Category, Adress, Place, Comment
from .forms import SignUpForm, ConnexionForm, UpdateProfile, PlaceSubmissionForm, CommentForm
from .utils import GetDepartementAndRegion, DoesKeyExists, GetNote
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

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

@login_required
def suggesting_new_place(request):
    my_user = request.user
    template = loader.get_template('application/suggesting-new-place.html')
    context = {'user': my_user}
    if request.method == 'POST':
        form = PlaceSubmissionForm(request.POST)
        # form.actual_user = my_user
        if form.is_valid():

            try:
                """Creating a new adress"""
                # print(form.data['postal_code'])
                my_departement_and_region = GetDepartementAndRegion(form.data['postal_code'])
                new_adress = Adress(postal_code=form.data['postal_code'], street_adress=form.data['street_adress'], departement=my_departement_and_region[0], region=my_departement_and_region[1], city=" ") 
                # this_substitute.save()
                # print(new_adress)
                new_adress.save()
                # print(my_departement_and_region[1])

                """Creating a new place"""
                new_place = Place(name=form.data['name'], contact_mail=form.data['contact_mail'], contact_phone=form.data['contact_phone'], can_be_seen=False, adress_id=new_adress.id, category_id=form.data['category'])
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

def all_places(request):
    places = Place.objects.all()
    print(places)
    context = {'places': places}
    template = loader.get_template('application/all-places.html')
    return HttpResponse(template.render(context, request=request))

def show_place(request, place_id):
    print("path is good")
    this_place = get_object_or_404(Place, pk=place_id)
    its_comments = Comment.objects.filter(place_id=this_place.id)
    # pos_reviews = its_comments.filter(score_global='P').count()
    # neg_reviews = its_comments.filter(score_global='N').count()
    # this_place.note_global = GetNote(pos_reviews, neg_reviews)
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
    # context = {}
    # template = loader.get_template('application/index.html')
    # return HttpResponse(template.render(context, request=request))

    # name = forms.CharField()
    # category = forms.ModelChoiceField(queryset = Category.objects.all())

    # street_adress = forms.CharField()
    # postal_code = forms.CharField(min_length=5, max_length=5)

    # contact_mail = forms.CharField()
    # contact_phone = forms.CharField()

    # comment = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20, "blank": True}))
    # score_global = forms.CharField(max_length=1)
    # can_you_enter = forms.BooleanField(required=False)
    # are_you_safe_enough = forms.BooleanField(required=False)
    # is_mixed_lockers = forms.BooleanField(required=False)
    # is_inclusive_lockers = forms.BooleanField(required=False)
    # has_respectful_staff = forms.BooleanField(required=False)