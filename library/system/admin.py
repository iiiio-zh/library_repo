from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db import models

from tinymce.widgets import TinyMCE
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User, BookCategory, Book, Notice

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin')
    list_filter = ('admin',)
    # UserAdminChangeForm, edit user
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('admin', 'librarian', 'member', 'active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    # UserAdminCreationForm, add user
    add_fieldsets = fieldsets
    
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

class BookAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title/Category", {'fields': ["book_title", "book_category"]}),
        ("Published Date", {'fields': ["book_published_date"]}),
        ("URL", {'fields': ["book_slug"]}),
        ("Summary", {"fields": ["book_summary"]}),
        ("Additional", {"fields": ["book_return_dateline", "book_returned_date", "book_borrowed_date", "book_borrowed", "book_borrowed_by"]})
    ]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
        }

class NoticeAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title", {'fields': ["notice_title"]}),
        ("Published Date", {'fields': ["notice_published"]}),
        ("Content", {'fields': ["notice_content"]})
    ]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
        }

# admin.site.register(TutorialSeries)
# admin.site.register(TutorialCategory)
# admin.site.register(Tutorial, TutorialAdmin)

admin.site.register(BookCategory)
admin.site.register(Book, BookAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(User, UserAdmin)



# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
