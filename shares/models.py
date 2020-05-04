from django.db import models
# python manage.py makemigrations
# python manage.py migrate
class Klins(models.Model):
    # id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=10, blank=True, verbose_name="码值")
    name = models.CharField(max_length=50, blank=True, verbose_name="名称")
    data = models.CharField(max_length=50000, blank=True, verbose_name="内容")
    flag = models.CharField(max_length=10, blank=True, verbose_name="k线类型")
    addtime = models.DateTimeField(verbose_name="添加时间", auto_now_add=True, blank=True)

# 对象的默认排序字段，获取对象列表时使用，升序ordering['time_added']，降序ordering['-time_added']
    class Meta:
        ordering = ['id']

    verbose_name = "K线信息表"
    verbose_name_plural = verbose_name
    db_table = "klins_info"

