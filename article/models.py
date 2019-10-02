from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager
# Create your models here.
from django.utils import timezone

class ArticleColumn(models.Model):
    title = models.CharField(max_length=100,blank = True)
    created = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title

class ArticlePost(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    body = models.TextField()
    total_views = models.PositiveIntegerField(default=0)
    column = models.ForeignKey(
        ArticleColumn,
        null = True,
        blank = True,
        on_delete=models.CASCADE,
        related_name='article',
    )
    tags = TaggableManager(blank=True)
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title
