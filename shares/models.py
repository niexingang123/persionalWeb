from django.db import models

class Klins(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=10, blank=True, verbose_name="码值")
    name = models.CharField(max_length=50, blank=True, verbose_name="名称")
    data = models.CharField(max_length=5000, blank=True, verbose_name="内容")
    addtime = models.DateTimeField(verbose_name="添加时间", auto_now_add=True, blank=True)
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        # some actions
        self.save()
    def save(self, force_insert=False, force_update=False, using=None,
    update_fields=None):
    # some actions
        self.name = self.name.capitalize() # 首字母大写
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
       update_fields=update_fields)
    def __repr__(self):
        return "UserProfile:{}".format(self.name)
    def __str__(self):
        return self.name
class Meta:
    ordering = ['time_added']
# 对象的默认排序字段，获取对象列表时使用，升序ordering['time_added']，降序ordering['-time_added']
verbose_name = "K线信息表"
verbose_name_plural = verbose_name
db_table = "kins_info"