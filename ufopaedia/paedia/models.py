from django.db import models

class Category(models.Model):
  name = models.CharField(max_length=20)
  image = models.CharField(max_length=200)

  def __unicode__(self):
    return "%s" % self.name

  def is_empty(self):
    subjects = Subject.objects.filter(category__exact=self.id)
    for subject in subjects:
      if not subject.is_empty():
        return False

    return True

class Subject(models.Model):
  name = models.CharField(max_length=20)
  research = models.BooleanField()
  category = models.ForeignKey(Category)

  def __unicode__(self):
    return "%s" % self.name

  def is_empty(self):
    articles = Article.objects.filter(subject__exact=self.id)
    for article in articles:
      if article.unlocked:
        return False

    return True


class Article(models.Model):
  caption = models.CharField(max_length=30)
  unlocked = models.BooleanField(default=False)
  image = models.CharField(max_length=200)
  text = models.TextField()
  code = models.CharField(max_length=20)
  subject = models.ForeignKey(Subject)
  level = models.PositiveSmallIntegerField()
  researched = models.BooleanField(default=False)
  read = models.BooleanField(default=False)

  def __unicode__(self):
    return "%s" % self.caption

  def split_to_paragraphs(self):
    return self.text.split("###")

class ResearchPoint(models.Model):
  code = models.CharField(max_length=200)
  token = models.PositiveSmallIntegerField()
  enabled = models.BooleanField(default=False)
  spent = models.BooleanField(default=False)
