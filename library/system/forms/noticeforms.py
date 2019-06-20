from django import forms
from django.utils import timezone

from system.models.notice import Notice

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
