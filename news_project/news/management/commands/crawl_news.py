import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Chạy tệp crawl.py để thu thập tin tức'

    def handle(self, *args, **kwargs):
        try:
            subprocess.run(['python3', '/Users/macbook/Desktop/web/news_project/vnbiz_taichinh.py'], check=True)
            self.stdout.write(self.style.SUCCESS('Thu thập tin tức thành công!'))
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR('Thu thập tin tức thất bại: {}'.format(e)))
