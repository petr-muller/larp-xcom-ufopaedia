from paedia.models import Category
from paedia.models import Subject
from paedia.models import Article
from paedia.models import ResearchPoint
from django.template import Context
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class WrappedCategory:
  def __init__(self, category):
    self.category = category
    self.empty = category.is_empty()

def index(request):
  categories = Category.objects.order_by('-name')

  category_list = []

  for category in categories:
      category_list.append(WrappedCategory(category))

  rp_count = len(ResearchPoint.objects.filter(enabled__exact=True).filter(spent__exact=False).order_by('-token'))

  context = Context({ 'category_list' : category_list,
                      'body_template' : 'main.html',
                      'page_title'    : 'UFOpaedia',
                      'rp_count'      : rp_count})
  return render(request, 'overframe.html', context)

def article_view(request, category_id, article_id=None):
  try:
    category = Category.objects.get(pk=category_id)
  except Category.DoesNotExist:
    raise Http404

  subjects = Subject.objects.filter(category__exact=category_id)

  if article_id is not None:
    article = Article.objects.get(pk=article_id)
    article.read = True
    article.save()
  else:
    article = None

  article_list = []
  for subject in subjects:
    articles = Article.objects.filter(subject__exact=subject).filter(unlocked__exact=True).order_by("-level")
    if subject.research:
      article_list.extend(articles)
    elif articles:
      article_list.append(articles[0])

  if article is None:
    article = article_list[0]

  rp = ResearchPoint.objects.filter(enabled__exact=True).filter(spent__exact=False).order_by('-token')

  context = Context({ 'category' : category,
                      'body_template' : "article.html",
                      'article_list' : article_list,
                      'article' : article,
                      'research_points' : len(rp)})
  return render(request, 'overframe.html', context)

def unlock(request):
  code = request.POST['code']
  try:
    article = Article.objects.get(code__exact=code)
    article.unlocked = True;
    article.save()
    return HttpResponseRedirect(reverse('paedia:article_view', args=(article.subject.category.id, article.id )))
  except Article.DoesNotExist:
    pass

  try:
    rp = ResearchPoint.objects.get(code__exact=code)
    if not rp.enabled:
      rp.enabled = True
      rp.save()

  except:
    pass

  return HttpResponseRedirect("/")


def research(request):
  code = request.POST['article']

  article = Article.objects.get(pk=code)
  article.researched = True
  article.save()

  try:
    article_above = Article.objects.filter(subject_id__exact=article.subject.id).filter(level__gt=article.level)[0]
    article_above.unlocked=True
    article_above.save();
  except Article.DoesNotExist:
    pass
  except IndexError:
    pass

  rp = ResearchPoint.objects.filter(enabled__exact=True).filter(spent__exact=False).order_by("-token")[0]
  rp.spent = True
  rp.save()

  return HttpResponseRedirect(reverse('paedia:article_view', args=(article.subject.category.id, article.id )))
