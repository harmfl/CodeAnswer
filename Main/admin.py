from django.contrib import admin
from .models import Num_of_Crawl


class NumOfCrawlAdmin(admin.ModelAdmin):
    list_display = ('user', 'csdn_count', 'cnblogs_count', 'juejin_count', 'github_count')  # 显示四个爬取数量字段和用户
    list_filter = ('user',)  # 可以根据用户进行过滤
    search_fields = ('user__username',)  # 允许根据用户名搜索
    ordering = ('user',)  # 默认按照用户排序


# 注册爬取数量模型
admin.site.register(Num_of_Crawl, NumOfCrawlAdmin)
