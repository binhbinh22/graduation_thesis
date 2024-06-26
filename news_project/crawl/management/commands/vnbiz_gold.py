import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Thu thập tin tức từ VNbiz'

    def handle(self, *args, **kwargs):
        try:
            subprocess.run(['python3', '/Users/macbook/Desktop/web/news_project/vnbiz_gold.py'], check=True)
            self.stdout.write(self.style.SUCCESS('Thu thập tin tức từ VNbiz thành công!'))
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f'Thu thập tin tức từ VNbiz thất bại: {str(e)}'))
