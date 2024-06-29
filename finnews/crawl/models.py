from django.db import models

class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Quản lý chủ đề"

    def __str__(self):
        return self.name

class Crawls(models.Model):
    AUTHOR_CHOICES = [
        ('VNexpress', 'VNexpress'),
        ('Vietnam Biz', 'Vietnam Biz'),
        ('Cafef', 'Cafef'),
        ('VnEconomy', 'VnEconomy'),
        ('Mobiagri', 'Mobiagri'),
        ('Thanh niên', 'Thanh niên')
    ]

    author = models.CharField(max_length=20, choices=AUTHOR_CHOICES)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    url = models.URLField()
    is_collected = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Thiết lập nguồn tin"

    def __str__(self):
        return self.author


# class Crawl(models.Model):
#     AUTHOR_CHOICES = [
#         ('VNexpress', 'VNexpress'),
#         ('Vietnam Biz', 'Vietnam Biz'),
#         ('Cafef', 'Cafef'),
#         ('VnEconomy', 'VnEconomy'),
#         ('Mobiagri', 'Mobiagri'),
#         ('Thanh niên', 'Thanh niên')
#     ]
#     TIME_CHOICES = [
#         ('Giá vàng', 'Giá vàng'),
#         ('Xăng dầu', 'Xăng dầu'),
#         ('Tài chính', 'Tài chính'),
#         ('Nông sản', 'Nông sản'),
#     ]
#     author = models.CharField(max_length=20, choices=AUTHOR_CHOICES)
#     # topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
#     topic = models.CharField(max_length=100, choices=TIME_CHOICES)
#     url = models.URLField()
#     is_collected = models.BooleanField(default=False)

#     class Meta:
#         verbose_name_plural = "Test"

#     def __str__(self):
#         return self.author


# from django.db import models

# class Topic(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()

#     class Meta:
#         verbose_name_plural = "Quản lý chủ đề"

#     def __str__(self):
#         return self.name
# class Crawl(models.Model):
#     # TIME_CHOICES = [
#     #     ('Giá vàng', 'Giá vàng'),
#     #     ('Xăng dầu', 'Xăng dầu'),
#     #     ('Tài chính', 'Tài chính'),
#     #     ('Nông sản', 'Nông sản'),
#     # ]
#     AUTHOR_CHOICES = [
#         ('VNexpress', 'VNexpress'),
#         ('Vietnam Biz', 'Vietnam Biz'),
#         ('Cafef', 'Cafef'),
#         ('VnEconomy', 'VnEconomy'),
#         ('Mobiagri','Mobiagri'),
#         ('Thanh niên','Thanh niên')
#     ]
#     # author = models.CharField(max_length=255)
#     author = models.CharField(max_length=20, choices=AUTHOR_CHOICES)
#     topic = models.ForeignKey(Topic, on_delete=models.CASCADE)  # Sử dụng ForeignKey để liên kết với mô hình Topic
#     #topic = models.CharField(max_length=100, choices=TIME_CHOICES)
#     url = models.URLField()
#     is_collected = models.BooleanField(default=False)


#     class Meta:
#         verbose_name_plural = "Thiết lập nguồn tin"

#     def __str__(self):
#         return f"{self.author} - {self.topic}"
