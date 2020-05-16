from django.db import models
# python manage.py makemigrations
# python manage.py migrate
class Klins(models.Model):
    id = models.IntegerField(primary_key=True)
    fid = models.IntegerField()
    code = models.CharField(max_length=10, blank=True, verbose_name="码值")
    name = models.CharField(max_length=50, blank=True, verbose_name="名称")
    data = models.CharField(max_length=50000, blank=True, verbose_name="内容")
    flag = models.CharField(max_length=10, blank=True, verbose_name="k线类型")
    addtime = models.DateTimeField(verbose_name="添加时间", auto_now_add=True, blank=True)

# 对象的默认排序字段，获取对象列表时使用，升序ordering['time_added']，降序ordering['-time_added']
    class Meta:
        verbose_name = "K线信息表"
        verbose_name_plural = verbose_name
        db_table = "klins_info"

    def short_data(self):
        if len(str(self.data)) > 100:
            return '{}...'.format(str(self.data)[0:100])
        else:
            return str(self.data)
    short_data.allow_tags = True

class Stocks(models.Model):
    id = models.IntegerField(primary_key=True)
    fid = models.IntegerField()
    code = models.CharField(max_length=10, blank=True, verbose_name="码值")
    name = models.CharField(max_length=10, blank=True, verbose_name="名称")
    industry = models.CharField(max_length=10, blank=True, verbose_name="行业")
    area = models.CharField(max_length=10, blank=True, verbose_name="地区")
    price_change = models.DecimalField(max_digits=10, decimal_places=2, blank=True, verbose_name="5日涨幅")
    pricediff = models.DecimalField(max_digits=10, decimal_places=2, blank=True, verbose_name="价格比")
    totals = models.DecimalField(max_digits=10, decimal_places=2, blank=True, verbose_name="总股本(亿)")
    data = models.CharField(max_length=50000, blank=True, verbose_name="k线数据")
    addtime = models.DateTimeField(verbose_name="添加时间", auto_now_add=True, blank=True)

# 对象的默认排序字段，获取对象列表时使用，升序ordering['time_added']，降序ordering['-time_added']
    class Meta:
        verbose_name = "股票信息表"
        verbose_name_plural = verbose_name
        db_table = "stocks_info"

    def short_data(self):
        if len(str(self.data)) > 100:
            return '{}...'.format(str(self.data)[0:100])
        else:
            return str(self.data)
    short_data.allow_tags = True

