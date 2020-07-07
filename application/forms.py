from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import User, Category, Adress, Place, Comment

User = get_user_model()


class SearchForm(forms.Form):
    query = forms.CharField(max_length=200)


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
        fields = ('username', 'gender', 'situation', 'about_me')


class PlaceSubmissionForm(forms.Form):
    name = forms.CharField()
    picture = forms.URLField(required=False)
    description = forms.CharField()
    website = forms.URLField(required=False)
    category = forms.ModelChoiceField(queryset = Category.objects.all())

    street_adress = forms.CharField()
    postal_code = forms.CharField(min_length=5, max_length=5)

    contact_mail = forms.CharField(required=False)
    contact_phone = forms.CharField(required=False)

    comment = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20, "blank": True}))

    NOTES_POSSIBLES= [
    ('P', 'Positive'),
    ('O', 'Neutre'),
    ('N', 'Négative'),
    ]

    score_global = forms.CharField(label='Evaluation', widget=forms.RadioSelect(choices=NOTES_POSSIBLES))
    can_you_enter = forms.BooleanField(required=False)
    are_you_safe_enough = forms.BooleanField(required=False)
    is_mixed_lockers = forms.BooleanField(required=False)
    is_inclusive_lockers = forms.BooleanField(required=False)
    has_respectful_staff = forms.BooleanField(required=False)


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20, "blank": True}))
    
    NOTES_POSSIBLES= [
    ('P', 'Positive'),
    ('O', 'Neutre'),
    ('N', 'Négative'),
    ]

    score_global = forms.CharField(label='Evaluation', widget=forms.RadioSelect(choices=NOTES_POSSIBLES))
    can_you_enter = forms.BooleanField(required=False)
    are_you_safe_enough = forms.BooleanField(required=False)
    is_mixed_lockers = forms.BooleanField(required=False)
    is_inclusive_lockers = forms.BooleanField(required=False)
    has_respectful_staff = forms.BooleanField(required=False)

    # def __init__(self, *args, **kwargs):
    #     self.fields['category_list'] = forms.ChoiceField(
    #         choices=[(cat.id, cat.name) for cat in Category.objects.all()],
    #         required=False,
    #         )

    class Meta:
        fields = ('comment', 'score_global', 'can_you_enter', 'are_you_safe_enough', 'is_mixed_lockers', 'is_inclusive_lockers', 'has_respectful_staff')