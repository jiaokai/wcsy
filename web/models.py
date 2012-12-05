# -- coding=utf-8 --
from django.db import models
from django.forms import ModelForm
from DjangoUeditor.models import UEditorField
from DjangoUeditor.forms import UEditorModelForm


# News {{{1
class m_news( models.Model ):
    s_title = models.CharField(u"标题", max_length=100, default=u"标题")
    s_sum = models.CharField(u"简述", max_length=100, default=u"简述")
    s_face = models.CharField(u"标题图片", max_length=100, blank=True)
    d_postdate = models.DateField(u"发布日期", auto_now_add=True)
    s_content = UEditorField(u"内容",height=400,width=720,imagePath="img/",imageManagerPath="img/",toolbars='full',options={"elementPathEnabled":True},filePath='upload',blank=True, default=u"新闻内容")
    i_status = models.IntegerField(u"状态", max_length=2, default=1)
    CATEGORY = ((1, u"公司新闻"), (2, u"行业动态"), (3, u"政策法规"), (4, u"活动专题"), (5, u"媒体报道"))
    i_category = models.IntegerField(u"分类", choices=CATEGORY, max_length=2, default=1)
    s_poster = models.CharField(u"发布人", max_length=20)

class f_news(UEditorModelForm):
    class Meta:
        model = m_news
        exclude = ('d_postdate', 'i_status', 's_poster',)

# products {{{1
class m_product_category( models.Model):
    s_cname = models.CharField(u"类别名称", max_length=50)
    s_sum = models.CharField(u"简述", max_length=100, blank=True, default=u"简述")
    i_count = models.IntegerField(u"数量", max_length=6, default=0)

    def __unicode__(self):
        return self.s_cname

class f_product_category(UEditorModelForm):
    class Meta:
        model = m_product_category
        exclude = ('i_count',)

class m_product( models.Model ):
    f_category = models.ForeignKey('m_product_category', verbose_name=u"分类")
    d_postdate = models.DateField(u"发布日期", auto_now_add=True)
    s_name = models.CharField(u"名称", max_length=100, default="名称")
    s_face = models.CharField(u"标题图片", max_length=100, blank=True)
    i_price = models.IntegerField(u"价格", max_length=10, default=0)
    s_intr = UEditorField(u"介绍",height=400,width=720,imagePath="img/",imageManagerPath="img/",toolbars='full',options={"elementPathEnabled":True},filePath='upload',blank=True, default=u"介绍")
    s_link_buy = models.CharField(u"购买链接", max_length=500, blank=True)
    i_status = models.IntegerField(u"状态", max_length=2, default=1)
    s_poster = models.CharField(u"发布人", max_length=20)

    def __unicode__(self):
        return self.s_name

class f_product(UEditorModelForm):
    class Meta:
        model = m_product
        exclude = ('s_face', 'i_status', 's_poster', )

# company {{{1
class m_options(models.Model):
    s_name = models.CharField(u"参数", max_length=20)
    s_content = UEditorField(u"介绍",height=400,width=720,imagePath="img/",imageManagerPath="img/",toolbars='full',options={"elementPathEnabled":True},filePath='upload',blank=True, default=u"介绍")
    i_status = models.IntegerField(u"状态", max_length=2, default=1)

class f_options(UEditorModelForm):
    class Meta:
        model = m_options
        exclude = ('s_name', 'i_status',)


# vim: foldmethod=marker
# vim: foldcolumn=2
