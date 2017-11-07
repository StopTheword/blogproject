# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length = 100)

	def __str__(self):
		return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
    	return self.name

class Post(models.Model):
    """文章的数据表"""
    #文章标题
    title = models.CharField(max_length=70) 
    #文章正文
    body = models.TextField()
    #创建时间
    created_time = models.DateTimeField()
    #修改时间
    modified_time = models.DateTimeField()
    #文章摘要,CharField的blank=true就允许为空值
    excerpt = models.CharField(max_length=200, blank=True)
    #文章与分类是一对多关系，
    #文章与标签是多对多关系，文章可以没有标签
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)
    #新增views字段记录阅读量,PositiveIntegerField类型的值只允许为整数或0
    views = models.PositiveIntegerField(default = 0)
    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
    author = models.ForeignKey(User)

    def __str__(self):
    	return self.title


    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk':self.pk})
    
    #定义内部类Meta,ordering属性用来指定文章排序方式
    class Meta:
        ordering = ['-created_time']  

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])  
        #update_fields参数告诉Django只更新数据库中views字段的值  

    #复写save()方法实现自动摘要
    def save(self, *args, **kwargs):
        #如果没有填写摘要
        if not self.excerpt:
            #实例化一个markdown类，用于渲染body文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite'
                ])   
            #先将markdown文本渲染成html文本
            #strip_tags 去掉HTML文本的全部HTML标签
            #从文本摘取前54的字符赋给excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        #调用父类的save方法将数据保存到数据库中
        super(Post,self).save(*args, **kwargs)           	





