from django import forms
from .models import *

from django.forms import ModelForm, SplitDateTimeField
from django.forms.widgets import Textarea, TextInput, SplitDateTimeWidget
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

class CelebritiesForm(ModelForm):
    class Meta:
        model = Celebrities
        # The Celebrities model may not have firstname/lastname fields anymore.
        # Keep nickname and imageurl. If bands still exists, it will be ignored
        # by the form unless present in the model; including it here would
        # raise an error when it's absent. To be safe, only list fields that
        # we know exist.
        fields = ['nickname', 'imageurl']
        widgets = {
            'nickname': TextInput(attrs={'class': 'form-control bg-light'}),
            # 'imageurl': forms.FileInput(attrs={'class': 'form-control bg-light', 'id': 'imageupload'}),
            'imageurl': forms.FileInput(attrs={
                'class': 'form-control bg-light', 'id': 'imageupload', 
                'accept': 'image/*'}),
        }

    def clean_data(self):
        cleaned_data = super().clean()
        # Perform custom validation here if needed
        return cleaned_data

    def clean(self):
        cleaned_data = super().clean()
        nickname = (cleaned_data.get('nickname') or '').strip()

        if nickname:
            qs = Celebrities.objects.filter(nickname__iexact=nickname)
            if self.instance and getattr(self.instance, 'pk', None):
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise ValidationError('A celebrity with the same nickname already exists.')

        return cleaned_data


class PlacesForm(ModelForm):
    class Meta:
        model = Places
        fields = ['name', 'googlemaplink', 'address', 'imageurl']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control bg-light'}),
            'googlemaplink': TextInput(attrs={'class': 'form-control bg-light'}),
            'address': Textarea(attrs={'class': 'form-control bg-light'}),
            # 'imageurl': forms.FileInput(attrs={'class': 'form-control bg-light', 'id': 'imageupload'}),
            'imageurl': forms.FileInput(attrs={
                'class': 'form-control bg-light', 'id': 'imageupload', 
                'accept': 'image/*'}),
        }

    def clean_data(self):
        cleaned_data = super().clean()

        return cleaned_data

    def clean(self):
        cleaned_data = super().clean()
        raw_name = cleaned_data.get('name') or ''
        name = raw_name.strip()
        # name = raw_name.strip().lower()

        if name:
            qs = Places.objects.filter(name__iexact=name)
            if self.instance and getattr(self.instance, 'pk', None):
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                # Raise a form-level validation error so it appears in non-field errors alert
                raise ValidationError('A place with the same name already exists.')

            # put the normalized name back so it will be saved in lowercase
            cleaned_data['name'] = name

        return cleaned_data


class SightingsForm(ModelForm):
    class Meta:
        model = Sightings
        fields = ['places', 'arrivaldate']
        # add-fields ==> ['celebrities', 'places', 'arrivaldate', 'addby_users', 'created_at']
        widgets = {
            'places': forms.Select(attrs={'class': 'form-control bg-light'}),
            'arrivaldate': forms.DateInput(attrs={'class': 'form-control bg-light', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        # Perform custom validation here if needed
        return cleaned_data


class SightingsForm2(ModelForm):
    class Meta:
        model = Sightings
        fields = ['celebrities', 'places', 'arrivaldate']
        # add-fields ==> ['celebrities', 'places', 'arrivaldate', 'addby_users', 'created_at']
        widgets = {
            'celebrities': forms.Select(attrs={'class': 'form-control bg-light'}),
            'places': forms.Select(attrs={'class': 'form-control bg-light'}),
            'arrivaldate': forms.DateInput(attrs={'class': 'form-control bg-light', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        # c = cleaned_data.get('celebrities')
        # p = cleaned_data.get('places')

        # if c and p:
        #     queryset = Sightings.objects.filter(celebrities=c, places=p)
        #     if self.instance and self.instance.pk:
        #         queryset = queryset.exclude(pk=self.instance.pk)

        #     if queryset.exists():
        #         raise forms.ValidationError(
        #             "this sighting has been added before"
        #         )

        return cleaned_data


# Bands model is not defined in models.py (commented out). If you later add
# a Bands model, you can recreate a BandsForm here.


class ProfileImageEditForm(ModelForm):
    class Meta:
        model = Users
        fields = ['imageurl']
        widgets = {
            'imageurl': forms.FileInput(attrs={
                'class': 'form-control bg-light', 'id': 'imageupload', 
                'style': 'display: none;', 'accept': 'image/*'}),
        }

    def clean(self):
        return super().clean()


class ProfileEditForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control bg-light'}),
            'last_name': TextInput(attrs={'class': 'form-control bg-light'}),
            'username': TextInput(attrs={'class': 'form-control bg-light'}),
        }

    def clean(self):
        return super().clean()


class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['rating', 'comment_text']
        widgets = {
            'comment_text': Textarea(attrs={'class': 'form-control bg-light', 'rows': 3}),
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
        }

    def clean_comment_text(self):
        txt = self.cleaned_data.get('comment_text', '') or ''
        if len(txt) > 2000:
            raise ValidationError('ความยาวต้องไม่เกิน 2000 ตัวอักษร')
        return txt

# ===== 
class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-light'})
    )
    password2 = forms.CharField(
        label='Password confirmation', 
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-light'})
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control bg-light'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control bg-light'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control bg-light'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        if username and username.lower() == "admin":
            # ถ้าเงื่อนไขผิด ให้ raise ValidationError
            raise forms.ValidationError("Username 'admin' is not allowed.")
        return cleaned_data


class CustomPasswordChangeForm(PasswordChangeForm):
    # * overwrite PasswordChangeForm
    old_password = forms.CharField(
        label="Old Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control bg-light'}
        )
    )

    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control bg-light'}
        )
    )

    new_password2 = forms.CharField(
        label="Confirm New Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control bg-light'}
        )
    )


