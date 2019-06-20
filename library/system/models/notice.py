from django.db import models
from django.utils import timezone

class Notice(models.Model):
    notice_title = models.CharField(max_length=200)
    notice_content = models.TextField()
    notice_published = models.DateTimeField('date published', default=timezone.now())
    notice_slug = models.CharField(max_length=200)
    def __str__(self):
        return self.notice_title
