from django.contrib import admin

# Register your models here.
from .models import ArticleColumn
from .models import ArticlePost
admin.site.register(ArticleColumn)
admin.site.register(ArticlePost)
