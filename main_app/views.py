from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.shortcuts import render
from .models import News, Article


def home(request):
    context = {
        'title': 'Stock Home',
        'news': News.objects.all(),
        'articles': Article.objects.all(),
    }
    return render(request, 'main_app/index.html', context)


class Home(ListView):
    model = News
    template_name = 'main_app/index.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'news'
    ordering = ['-date_posted']
    paginate_by = 3
