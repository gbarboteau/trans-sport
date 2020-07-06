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


    # comment = models.TextField()
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # place = models.ForeignKey(Place, on_delete=models.CASCADE)
    # date = models.DateTimeField()
    # score_global = models.CharField(max_length=1)
    # can_you_enter = models.BooleanField()
    # are_you_safe_enough = models.BooleanField()
    # is_mixed_lockers = models.BooleanField()
    # is_inclusive_lockers = models.BooleanField()
    # has_respectful_staff = models.BooleanField()


    # region = models.TextField()
    # departement = models.TextField()
    # postal_code = models.TextField(max_length=5)
    # city = models.TextField()
    # street_adress = models.TextField()

    # name = models.TextField()
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # adress = models.ForeignKey(Adress, on_delete=models.CASCADE)
    # contact_mail = models.TextField()
    # contact_phone = models.TextField()
    # can_be_seen = models.BooleanField(default=False)