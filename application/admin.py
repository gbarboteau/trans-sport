from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from application.models import User, Category, Adress, Place, Comment, Profile


class UserAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.fieldsets = ((None, {'fields': ('username', 'email', 'last_login', 'user_permissions', 'is_superuser', 'is_staff', 'is_active', 'gender', 'about_me'),}),)
            self.readonly_fields = []
        else:
            self.fieldsets = ((None, {'fields': ('username', 'email', 'last_login', 'is_staff', 'is_active', 'gender', 'about_me'),}),)
            self.readonly_fields = ['username', 'email', 'last_login', 'is_staff', 'gender', 'about_me',]
        return super(UserAdmin,self).get_form(request, obj=None, **kwargs)


class CategoryAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.fieldsets = ((None, {'fields': ('name', 'icon',),}),)
            self.readonly_fields = []
        else:
            self.fieldsets = ((None, {'fields': ('name', 'icon',),}),)
            self.readonly_fields = ['name', 'icon',]
        return super(CategoryAdmin,self).get_form(request, obj=None, **kwargs)


class PlaceAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.fieldsets = ((None, {'fields': ('name', 'picture', 'description', 'website', 'contact_mail', 'contact_phone', 'can_be_seen', 'adress', 'category'),}),)
            self.readonly_fields = []
        else:
            self.fieldsets = ((None, {'fields': ('name', 'picture', 'description', 'website', 'contact_mail', 'contact_phone', 'can_be_seen', 'adress', 'category'),}),)
            self.readonly_fields = []
        return super(PlaceAdmin,self).get_form(request, obj=None, **kwargs)


class CommentAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.fieldsets = ((None, {'fields': ('comment', 'date', 'score_global', 'can_you_enter', 'are_you_safe_enough', 'is_mixed_lockers', 'has_respectful_staff', 'place_id', 'user_id'),}),)
            self.readonly_fields = ['comment', 'date', 'score_global', 'can_you_enter', 'are_you_safe_enough', 'is_mixed_lockers', 'has_respectful_staff', 'place_id', 'user_id']
        else:
            self.fieldsets = ((None, {'fields': ('comment', 'date', 'score_global', 'can_you_enter', 'are_you_safe_enough', 'is_mixed_lockers', 'has_respectful_staff', 'place_id', 'user_id'),}),)
            self.readonly_fields = ['comment', 'date', 'score_global', 'can_you_enter', 'are_you_safe_enough', 'is_mixed_lockers', 'has_respectful_staff', 'place_id', 'user_id']
        return super(CommentAdmin,self).get_form(request, obj=None, **kwargs)


class AdressAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.fieldsets = ((None, {'fields': ('region', 'departement', 'postal_code', 'city', 'street_adress',),}),)
            self.readonly_fields = []
        else:
            self.fieldsets = ((None, {'fields': ('region', 'departement', 'postal_code', 'city', 'street_adress',),}),)
            self.readonly_fields = []
        return super(AdressAdmin,self).get_form(request, obj=None, **kwargs)


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Adress, AdressAdmin)
admin.site.register(Profile)