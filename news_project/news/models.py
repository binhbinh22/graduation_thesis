
from django.db import models

class News(models.Model):
    TIME_CHOICES = [
        ('Giá vàng', 'Giá vàng'),
        ('Xăng dầu', 'Xăng dầu'),
        ('Tài chính', 'Tài chính'),
        ('Nông sản', 'Nông sản'),
        ('Thực phẩm', 'Thực phẩm'),
    ]
    id = models.AutoField(primary_key=True)
    time = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField()
    topic = models.CharField(max_length=100, choices=TIME_CHOICES)
    author = models.CharField(max_length=100)
    link_img = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=[('guest', 'Guest'), ('admin', 'Admin')], default='guest')


class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class NewsTag(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

# class UserTag(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
