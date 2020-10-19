from django import forms
from .models import BlogPost
from .models import Comment

class BlogPostForm(forms.Form):
	title = forms.CharField()
	slug = forms.SlugField()
	content = forms.CharField(widget=forms.Textarea)


class BlogPostModelForm(forms.ModelForm):
	class Meta:
		model = BlogPost
		fields = ['title', 'slug','image', 'content','publish_date']
	
	def clean_title(self, *args, **kwargs): # this is a proper method and to named like this only

		title = self.cleaned_data.get('title')
		# print(dir(self))
		# we want use the same title while we update
		instance = self.instance
		# qs = BlogPost.objects.filter(title= title) # this is case sensetive
		qs = BlogPost.objects.filter(title__iexact= title) # this is not case sensetive

		print(title)
		
		if instance is not None:
			qs = qs.exclude(pk=instance.pk)

		if qs.exists():
			raise forms.ValidationError("title already used")
		return title


class CommentForm(forms.Form):
	content = forms.CharField()

class CommentModelForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['content']

	