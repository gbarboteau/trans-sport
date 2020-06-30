from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models import Avg
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    """Model for a customized user model"""
    gender = ArrayField(models.CharField(max_length=255), default=False)
    situation = ArrayField(models.CharField(max_length=255), default=False)
    is_admin = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    about_me = models.TextField(blank=True)


class Category(models.Model):
    """Model for the categories we want to add 
    in our database
    """
    name = models.TextField()
    icon = models.TextField()

    def __str__(self):
        return self.name


class Adress(models.Model):
    """Model for adresses"""
    region = models.TextField()
    departement = models.TextField()
    postal_code = models.TextField(max_length=5)
    city = models.TextField()
    street_adress = models.TextField()


class Place(models.Model):
    """Model for the places on the App"""
    class Meta:
        constraints = [models.UniqueConstraint(fields=['category', 'adress'], name='saved_place')]

    name = models.TextField()
    picture = models.TextField(blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    adress = models.ForeignKey(Adress, on_delete=models.CASCADE)
    website = models.TextField(blank=True)
    contact_mail = models.TextField(blank=True)
    contact_phone = models.TextField(blank=True)
    can_be_seen = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Comment(models.Model):
    """Model for the comments, linked to a given
    User, with their opinion and scores.
    """
    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'place'], name='saved_comment')]

    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    score_global = models.CharField(max_length=1)
    can_you_enter = models.BooleanField()
    are_you_safe_enough = models.BooleanField()
    is_mixed_lockers = models.BooleanField()
    is_inclusive_lockers = models.BooleanField()
    has_respectful_staff = models.BooleanField()

    def __str__(self):
        return (self.user.username + " " + self.place.name)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()