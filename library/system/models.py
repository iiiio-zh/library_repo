import datetime

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone

from .choices import *
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None,):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.first_name = first_name
        user.last_name = last_name
        user.member = True
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_librarianuser(self, email, password, first_name, last_name):
        """
        Creates and saves a librarian user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.first_name = first_name
        user.last_name = last_name
        user.librarian = True
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password, first_name, last_name):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,

        )
        user.first_name = first_name
        user.last_name = last_name
        user.librarian = True
        user.admin = True
        user.save(using=self._db)
        return user

# https://www.codingforentrepreneurs.com/blog/how-to-create-a-custom-django-user-model
class User(AbstractBaseUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    active = models.BooleanField(default=True)
    librarian = models.BooleanField(default=False) # a admin user; non super-user
    member = models.BooleanField(default=False)
    admin = models.BooleanField(default=False) # a superuser
    fine = models.FloatField(default=0)
    objects = UserManager()
    # notice the absence of a "Password field", that's built in.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.
    def get_full_name(self):
        # The user is identified by their email address
        return self.email
    def get_short_name(self):
        # The user is identified by their email address
        return self.email
    def __str__(self):              # __unicode__ on Python 2
        return self.email
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    @property
    def is_member(self):
        "Is the user a member?"
        return self.member
    @property
    def is_staff(self):
        "Is the user a librarian?"
        return self.librarian
    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin
    @property
    def is_active(self):
        "Is the user active?"
        return self.active

class Notice(models.Model):
    notice_title = models.CharField(max_length=200)
    notice_content = models.TextField()
    notice_published = models.DateTimeField('date published', default=timezone.now())
    notice_slug = models.CharField(max_length=200)
    def __str__(self):
        return self.notice_title

class BookCategory(models.Model):
    book_category = models.CharField(max_length=200)
    book_slug = models.CharField(max_length=200, default=1)
    class Meta():
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.book_category

class Book(models.Model):
    book_title = models.CharField(max_length=200)
    book_author = models.CharField(max_length=200)
    book_published_date = models.DateTimeField('date published', default=None, null=True, blank=True)
    book_category = models.ForeignKey(BookCategory, default=None, verbose_name="Category", on_delete=models.SET_DEFAULT)
    book_summary = models.TextField(default=None, null=True, blank=True)
    book_slug = models.CharField(max_length=200, default=1)
    book_return_dateline = models.DateTimeField('return dateline', default=None, null=True, blank=False)
    book_returned_date = models.DateTimeField('date returned', default=None, null=True, blank=True)
    book_borrowed_date = models.DateTimeField('date borrowed', default=None, null=True, blank=True)
    book_reserved = models.BooleanField(default=False)
    book_borrowed = models.BooleanField(default=False)
    book_borrowed_by = models.ForeignKey(User, default=None, on_delete=models.SET_DEFAULT, blank=False, null=True, related_name="borrowed_user")
    book_reserved_by = models.ForeignKey(User, default=None, on_delete=models.SET_DEFAULT, blank=False, null=True, related_name="reserved_user")
    book_reserved_date = models.DateTimeField('date reserved', default=None, null=True, blank=True)
    book_reservation_end_date = models.DateTimeField('reservation end', default=None, null=True, blank=True)
    book_active = models.BooleanField(default=True)
    book_position_section = models.CharField(max_length=20, choices=SECTION_CHOICES, default=None,)
    book_position_row = models.CharField(max_length=20, choices=ROW_CHOICES, default=None,)
    book_position_rack = models.CharField(max_length=20, choices=RACK_CHOICES, default=None,)
    book_position_rack_level = models.CharField(max_length=20, choices=RACK_LEVEL_CHOICES, default=None,)
    def make_slug(self, book_title):
        slug = book_title.replace(" ", "")
        slug = slug.lower()
        return slug
    def get_date(self):
        return self.modified.date()
    def is_overdue(self):
        if self.book_borrowed:
            duration = timezone.now() - self.book_return_dateline
            if duration > datetime.timedelta(seconds=1):
                return True
            else:
                return False
        else:
            return False
    def can_be_renewed(self):
        if self.book_borrowed:
            duration = self.book_return_dateline - timezone.now()
            if duration < datetime.timedelta(days=5):
                return True
            else:
                return False
        else:
            return False
    def __str__(self):
        return self.book_title

# class History(models.Model):
#     book_title = models.ForeignKey(User, default=None, on_delete=models.SET_DEFAULT)
#     book_returned_date = models.DateTimeField('date returned', default=None, null=True, blank=True)
#     book_borrowed_date = models.DateTimeField('date borrowed', default=None, null=True, blank=True)
#     book_reserved = models.BooleanField(default=False)
#     book_borrowed = models.BooleanField(default=False)
#     book_borrowed_by = models.ForeignKey(User, default=None, on_delete=models.SET_DEFAULT, blank=False, null=True, related_name="borrowed_user")
#     book_reserved_by = models.ForeignKey(User, default=None, on_delete=models.SET_DEFAULT, blank=False, null=True, related_name="reserved_user")
#     book_reserved_date = models.DateTimeField('date reserved', default=None, null=True, blank=True)
