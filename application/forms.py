from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import User, Category, Adress, Place, Comment

User = get_user_model()

class SearchForm(forms.Form):
    """Permet d'effectuer une recherche de lieu"""
    query = forms.CharField(max_length=200)


class SignUpForm(UserCreationForm):
    """Gère la création d'un compte utilisateur"""
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=200)

    GENDERS = (
        ("Femme trans", "Femme trans"),
        ("Femme cis", "Femme cis"),
        ("Homme trans", "Homme trans"),
        ("Homme cis", "Homme cis"),
        ("Personne non-binaire", "Personne non-binaire"),
        ("Autre identité", "Autre identité")
    )
    gender = forms.CharField(label='Genre', widget=forms.Select(choices=GENDERS, attrs={'class': 'inline-radio-block'}))

    about_me = forms.CharField(widget=forms.Textarea(attrs={"rows":7, "cols":50, "blank": True}), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'gender', 'password1', 'password2', )
        # fields = ('username', 'email', 'is_woman', 'is_man', 'is_other', 'is_trans', 'is_cis', 'is_nb', 'password1', 'password2', )


class ConnexionForm(forms.Form):
    """Gère la connexion des utilisateurs"""
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class UpdateProfile(UserChangeForm):
    """Permet de mettre à jour les informations de profil"""
    username = forms.CharField(max_length=30)
    about_me = forms.CharField(widget=forms.Textarea(attrs={"rows":7, "cols":50, "blank": True}), required=False)

    GENDERS = (
        ("Femme trans", "femme trans"),
        ("Femme cis", "femme cis"),
        ("Homme trans", "homme trans"),
        ("Homme cis", "homme cis"),
        ("Personne non-binaire", "personne non-binaire"),
        ("Autre identité", "autre identité")
    )
    gender = forms.CharField(label='Genre', widget=forms.Select(choices=GENDERS))

    class Meta:
        model = User
        fields = ('username', 'gender', 'about_me')


class PlaceSubmissionForm(forms.Form):
    """Permet de suggérer l'ajout d'un lieu (avec l'ajout
    d'un premier avis)
    """
    NOTES_POSSIBLES= [
    ('P', 'Positive'),
    ('O', 'Neutre'),
    ('N', 'Négative'),
    ]

    name = forms.CharField()
    picture = forms.URLField(required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":7, "cols":50, "blank": True}))
    website = forms.URLField(required=False)
    category = forms.ModelChoiceField(queryset = Category.objects.all())
    street_adress = forms.CharField()
    postal_code = forms.CharField(min_length=5, max_length=5)
    contact_mail = forms.CharField(required=False)
    contact_phone = forms.CharField(required=False)
    comment = forms.CharField(widget=forms.Textarea(attrs={"rows":7, "cols":50, "blank": True}))
    score_global = forms.CharField(label='Evaluation', widget=forms.Select(choices=NOTES_POSSIBLES))
    can_you_enter = forms.BooleanField(required=False)
    are_you_safe_enough = forms.BooleanField(required=False)
    is_mixed_lockers = forms.BooleanField(required=False)
    is_inclusive_lockers = forms.BooleanField(required=False)
    has_respectful_staff = forms.BooleanField(required=False)


class CommentForm(forms.Form):
    """Permet d'ajouter un avis (ou de l'éditer)"""
    NOTES_POSSIBLES= [
    ('P', 'Positive'),
    ('O', 'Neutre'),
    ('N', 'Négative'),
    ]

    comment = forms.CharField(widget=forms.Textarea(attrs={"rows":7, "cols":50, "blank": True}))
    score_global = forms.CharField(label='Evaluation', widget=forms.Select(choices=NOTES_POSSIBLES))
    can_you_enter = forms.BooleanField(required=False)
    are_you_safe_enough = forms.BooleanField(required=False)
    is_mixed_lockers = forms.BooleanField(required=False)
    is_inclusive_lockers = forms.BooleanField(required=False)
    has_respectful_staff = forms.BooleanField(required=False)

    class Meta:
        fields = ('comment', 'score_global', 'can_you_enter', 'are_you_safe_enough', 'is_mixed_lockers', 'is_inclusive_lockers', 'has_respectful_staff')
