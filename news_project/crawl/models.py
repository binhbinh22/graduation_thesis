from django.db import models

class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_show = models.BooleanField(default=True)
    # tags = models.ManyToManyField('GroupTag', through='TopicTag')
    class Meta:
        verbose_name_plural = "Quản lý chủ đề"

    def __str__(self):
        return self.name

# class GroupTag(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     class Meta:
#         verbose_name_plural = "Thiết lập nhóm Tag "

#     def __str__(self):
#         return self.name

# class TopicTag(models.Model):
#     topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
#     grouptag = models.ForeignKey(GroupTag, on_delete=models.CASCADE)
#     class Meta:
#         unique_together = ('topic', 'grouptag')
#         verbose_name_plural = "Quản lý chủ đề-nhóm Tag"

class Crawl(models.Model):
    AUTHOR_CHOICES = [
        ('VNexpress', 'VNexpress'),
        ('Vietnam Biz', 'Vietnam Biz'),
        ('Cafef', 'Cafef'),
        ('VnEconomy', 'VnEconomy'),
        ('Mobiagri', 'Mobiagri'),
        ('Thanh niên', 'Thanh niên'),
        ('Tapchicongthuong','Tạp chí công thương'),
        ('dantri','Dân trí')
    ]
    author = models.CharField(max_length=20, choices=AUTHOR_CHOICES)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    url = models.URLField()
    is_extract = models.BooleanField(default=True)

    # is_collecteds = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Thiết lập thu thập tin"

    def __str__(self):
        return f"{self.author} - {self.topic}"
