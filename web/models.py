# -- coding=utf-8 --
from django.db import models
from django.forms import ModelForm
from DjangoUeditor.models import UEditorField
from DjangoUeditor.forms import UEditorModelForm


# News {{{1
class m_news( models.Model ):
    s_title = models.CharField(u"标题", max_length=100, default=u"标题")
    d_postdate = models.DateField(u"发布日期", auto_now_add=True)
    s_content = UEditorField(u"内容",height=400,width=720,imagePath="img/",imageManagerPath="img/",toolbars='full',options={"elementPathEnabled":True},filePath='upload',blank=True, default=u"新闻内容")
    i_status = models.IntegerField(u"状态", max_length=2, default=1)
    s_poster = models.CharField(u"发布人", max_length=20)

class f_news(UEditorModelForm):
    class Meta:
        model = m_news
        exclude = ('d_postdate', 'i_status', 's_poster',)

# vim: foldmethod=marker
# vim: foldcolumn=2
