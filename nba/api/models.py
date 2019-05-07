from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=30, null=True)
    url = models.URLField(null=True)
    published_time = models.DateTimeField(null=True)
    news_source = models.CharField(max_length=30, null=True)
    news_reporter = models.CharField(max_length=30, null=True)
    news_type = models.CharField(max_length=30, null=True)
    news_content = models.TextField(null=True)





