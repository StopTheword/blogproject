from django import template
from django.db.models.aggregates import Count
from ..models import Post, Category,Tag

register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]


@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
	#Count计算分类下的文章数，其接受的参数为需要计数的模型的名称
	#Category.objects.annotate会返回数据库中的全部记录,但同时又可以做一些额外的事情
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

#标签云
@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts = Count('post')).filter(num_posts__gt=0)    