from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

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
