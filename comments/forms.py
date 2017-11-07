from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment #表明此表单对应的数据库模型是Comment
		fields = ['name', 'email','url','text'] 
		#指定了表单需要显示的字段
