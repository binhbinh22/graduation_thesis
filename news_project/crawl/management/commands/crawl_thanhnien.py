import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Thu thập tin tức từ thanh niên'

    def handle(self, *args, **kwargs):
        try:
            subprocess.run(['python3', '/Users/macbook/Desktop/web/news_project/thanhnien.py'], check=True)
            self.stdout.write(self.style.SUCCESS('Thu thập tin tức từ báo Thanh niên thành công!'))
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f'Thu thập tin tức từ Thanh niên thất bại: {str(e)}'))