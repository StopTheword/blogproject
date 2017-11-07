from django.shortcuts import render,get_object_or_404, redirect
from blog.models import Post

from .models import Comment
from .forms import CommentForm

# Create your views here.

def post_comment(request, post_pk):
	post = get_object_or_404(Post, pk=post_pk)

	if request.method == 'POST':
		form = CommentForm(request.POST)
		#调用form.is_valid()方法自动检查表单数据是否符合格式要求
		if form.is_valid():
			#commit=False的作用更仅仅是利用表单的数据生成Comment
			#模型类的实例，但还不保存评论数据到数据库
			comment = form.save(commit = False)
			#将评论和被评论的文章关联起来
			comment.post = post
			#最终将评论数据保存在数据库，调用模型实例的save方法
			comment.save()
			#重定向到post的详情页
			return redirect(post)
		else:
		    comment_list = post.comment_set.all()
		    context = {
		        'post': post,
		        'form': form,
		        'comment_list': comment_list
		    }	
		    return render(request, 'blog/detail.html',context=context)


	return redirect(post)#不是post请求重新定向到文章详情页    		
