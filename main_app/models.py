from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from PIL import Image


class News(models.Model):
    title = models.CharField(max_length=256)
    source = models.CharField(max_length=1000)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_news.png', upload_to='news_pics')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        
        if img.height > 1024 or img.width > 1024:
            output_size = (1024, 1024)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('news-detail', kwargs={'pk': self.pk})

    def __str__(self):
        if len(self.title) > 25:
            return str(self.title)[:23] + '...'
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=256)
    source = models.CharField(max_length=1000)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    image = models.ImageField(default='default_article.png', upload_to='article_pics')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        
        if img.height > 1024 or img.width > 1024:
            output_size = (1024, 1024)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('news-detail', kwargs={'pk': self.pk})

    def __str__(self):
        if len(self.title) > 25:
            return str(self.title)[:23] + '...'
        return self.title