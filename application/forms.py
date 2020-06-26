from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpForm(UserCreationForm):
    """Form handling users creating an account"""
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=200)

    GENDERS = (
        ("Femme", "femme"),
        ("Homme", "homme"),
        ("Autre", "autre")
    )
    gender = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=GENDERS)

    SITUATIONS = (
        ("Trans", "trans"),
        ("Cis", "cis"),
        ("Non-binaire", "non-binaire")
    )
    situation = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=SITUATIONS)

    class Meta:
        model = User
        fields = ('username', 'email', 'gender', 'situation', 'password1', 'password2', )
        # fields = ('username', 'email', 'is_woman', 'is_man', 'is_other', 'is_trans', 'is_cis', 'is_nb', 'password1', 'password2', )


class ConnexionForm(forms.Form):
    """Form handling users logging in"""
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class UpdateProfile(UserChangeForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=200)
    about_me = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20, "blank": True}), required=False)

    GENDERS = (
        ("Femme", "femme"),
        ("Homme", "homme"),
        ("Autre", "autre")
    )
    gender = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=GENDERS)

    SITUATIONS = (
        ("Trans", "trans"),
        ("Cis", "cis"),
        ("Non-binaire", "non-binaire")
    )
    situation = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=SITUATIONS)

    class Meta:
        model = User
        fields = ('username', 'email', 'gender', 'situation', 'about_me')
