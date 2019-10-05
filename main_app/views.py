from django.shortcuts import render
from .models import News, Article


def home(request):
    last_90_news = News.objects.filter().order_by('-id')[:9][::-1]
    last_90_news_sorted = [[last_90_news[i], last_90_news[i+1],
                            last_90_news[i+2]] for i in range(0, len(last_90_news), 3)]
    context = {
        'title': 'Stock Home',
        'news': last_90_news_sorted,
        'articles': Article.objects.all(),
    }
    return render(request, 'main_app/index.html', context)
