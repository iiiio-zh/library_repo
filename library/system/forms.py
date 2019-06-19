import datetime
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils import timezone


from .models import User, Book, Notice

# https://www.codingforentrepreneurs.com/blog/how-to-create-a-custom-django-user-model
# class LoginForm(auth.forms.AuthenticationForm):
#     username = forms.CharField(label=_("Username"), max_length=30,
#                                widget=forms.TextInput(attrs={'class': 'loginput'}))

class AddNoticeForm(forms.ModelForm):
    class Meta():
        model = Notice
        fields = ('notice_title', 'notice_content')
    def save(self, commit=True):
        instance = super(AddNoticeForm, self).save(commit=False)
        instance.published = timezone.now()
        if commit:
            instance.save()
        return instance

class AddBookForm(forms.ModelForm):
    book_published_date = forms.DateField(required = False, widget=forms.SelectDateWidget(years=range(1300, 2100)))
    class Meta():
        model = Book
        fields = ('book_title', 'book_author', 'book_category', 'book_summary', 'book_published_date',
                  'book_position_section', 'book_position_row', 'book_position_rack',
                  'book_position_rack_level')

class LendBookForm(forms.ModelForm):
    class Meta():
        model = Book
        fields = ('book_borrowed_by',)

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    class Meta():
        model = User
        fields = ('email',)
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'email')
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'active', 'member', 'librarian', 'admin')
    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
