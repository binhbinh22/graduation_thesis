from django.db import models

class Crawl(models.Model):
    TIME_CHOICES = [
        ('Giá vàng', 'Giá vàng'),
        ('Xăng dầu', 'Xăng dầu'),
        ('Tài chính', 'Tài chính'),
        ('Nông sản', 'Nông sản'),
    ]
    author = models.CharField(max_length=255)
    topic = models.CharField(max_length=100, choices=TIME_CHOICES)
    url = models.URLField()
    class Meta:
        verbose_name_plural = "Thu thập tin tức"

    def __str__(self):
        return f"{self.author} - {self.topic}"
