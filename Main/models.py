from django.db import models
from Login.models import *

# Create your models here.
class Num_of_Crawl(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='crawl_data')

    # 这四个字段存储各个网站的爬取数量,默认值为5
    csdn_count = models.IntegerField(default=5)
    cnblogs_count = models.IntegerField(default=5)
    juejin_count = models.IntegerField(default=5)
    github_count = models.IntegerField(default=5)

    def __str__(self):
        return f"Data for {self.user.username}"
