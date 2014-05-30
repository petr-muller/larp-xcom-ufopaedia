from django.contrib import admin
from paedia.models import Category
from paedia.models import Article
from paedia.models import Subject
from paedia.models import ResearchPoint

admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Subject)
admin.site.register(ResearchPoint)
