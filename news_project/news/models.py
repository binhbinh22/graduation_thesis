from django.db import models
from django.contrib.auth.models import User


class News(models.Model):
    # TIME_CHOICES = [
    #     ('Giá vàng', 'Giá vàng'),
    #     ('Xăng dầu', 'Xăng dầu'),
    #     ('Tài chính', 'Tài chính'),
    #     ('Nông sản', 'Nông sản'),
    # ]
    id = models.AutoField(primary_key=True)
    time = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField()
    topic = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    link_img = models.CharField(max_length=255, blank=True, null=True)    
    is_featured = models.BooleanField(default=False)  
    info_extrac = models.JSONField(null=True, blank=True)  
    tags = models.ManyToManyField('Tag', through='NewsTag')
    # searchs =models.ManyToManyField('Search', through='NewsSearch')
    class Meta:
        verbose_name_plural = "Quản lý tin tức"
    def __str__(self):
        return self.title

class Reason(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_show = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Nguyên nhân"

    def __str__(self):
        return self.name

class KeyReason(models.Model):
    name = models.CharField(max_length=100)
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Từ khoá nguyên nhân"

    def __str__(self):
        return self.name


class NewsReason(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    keyreasons = models.ForeignKey(KeyReason, on_delete=models.CASCADE)
    sentiment = models.CharField(max_length=100, blank=True, null=True )
    def reason(self):
        return self.keyreasons.reason.name
    class Meta:
        verbose_name_plural = "Quản lý Nguyên nhân- Tin tức"


class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    newss = models.ManyToManyField('News', through='NewsTag')
    class Meta:
        verbose_name_plural = "Tinh chỉnh Tags thủ công"
    def __str__(self):
        return self.name

class NewsTag(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    relation = models.CharField(max_length=100, blank=True, null=True )

    class Meta:
        unique_together = ('news', 'tag','relation')
        verbose_name_plural = "Quản lý Tag- Tin tức"
    
# class Search(models.Model):
#     name = models.CharField(max_length=100)
#     newss = models.ManyToManyField('News', through='NewsSearch')
#     class Meta:
#         verbose_name_plural = "Từ khoá tìm kiếm"
#     def __str__(self):
#         return self.name
    
# class NewsSearch(models.Model):
#     news = models.ForeignKey(News, on_delete=models.CASCADE)
#     search = models.ForeignKey(Search, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('news', 'search')


class UserTag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.tag.name}"

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Lịch sử đọc tin"
    def __str__(self):
        return f"{self.user.username} - {self.news.title}"

class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    news = models.ForeignKey(News, on_delete=models.CASCADE, default=1)
    class Meta:
        verbose_name_plural = "Lưu tin tức"
    def __str__(self):
        return f"{self.user.username} - {self.news.title}"

