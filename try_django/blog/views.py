from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import Http404 
from .models import BlogPost, Comment
from .form import BlogPostModelForm, CommentModelForm
# from django.utils import timezone
# from .form import BlogPostForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

def blog_post_list_view(request):
	# now = timezone.now()
	# qs = BlogPost.objects.all()
	qs = BlogPost.objects.published()
	# qs = BlogPost.objects.all().published()
	# qs = BlogPost.objects.filter(publish_date__lte=now)

	if request.user.is_authenticated:
		my_qs = BlogPost.objects.filter(user=request.user)
		qs = (qs | my_qs).distinct()


	template_name = 'blog/list.html'
	context = {"object_list":qs}
	return render(request,template_name,context)

# @login_required      # this will wrap the below method and check a if user is login or not      
# @staff_member_required # just as above but staff permission required
@login_required 
def blog_post_create_view(request):

	form = BlogPostModelForm(request.POST or None, request.FILES or None)
	
	if form.is_valid():
		# print(dir(form))
		# form.save()  saving the form directly
		obj = form.save(commit= False) # commit false will not save this
		# obj.title = form.cleaned_data.get('title') # + '0'
		obj.user = request.user
		obj.save()
		form = BlogPostModelForm()

	template_name = 'blog/form.html'
	context = {"form":form,}
	return render(request,template_name,context)

# @staff_member_required
@login_required 
def blog_post_update_view(request, slug):
	obj = get_object_or_404(BlogPost, slug = slug)
	form = BlogPostModelForm(request.POST or None, instance=obj)
	if form.is_valid():
		form.save()
		return redirect("/blog/"+slug)
	template_name = 'blog/form.html'

	context = {"form": form, "title": f"Update-{obj.title}" }
	return render(request,template_name,context)

	
def blog_post_detail_view(request, slug):
	obj = get_object_or_404(BlogPost, slug = slug)
	template_name = 'blog/detail.html'
	comments = reversed(Comment.objects.filter(blog=obj.id))
	context = {"object":obj, "comments":comments}
	return render(request,template_name,context)

# @staff_member_required
@login_required 
def blog_post_delete_view(request, slug):
	obj = get_object_or_404(BlogPost, slug = slug)
	template_name = 'blog/delete.html'
	if request.method == 'POST':
		obj.delete()
		return redirect("/blog")
	context = {"object":obj}
	return render(request,template_name,context)

# --------------------------------------------------------------
@login_required
def comment_create_view(request,slug):
	form = CommentModelForm(request.POST or None)

	if form.is_valid():
		obj = form.save(commit= False) # commit false will not save this
		obj.blog_id  = BlogPost.objects.filter(slug=slug).first().id
		# print(request.user)
		obj.user = request.user
		obj.save()
		
		return redirect("/blog/"+slug)

	template_name = 'blog/form.html'
	context = {"form":form,}
	return render(request,template_name,context)
# --------------------------------------------------------------
@login_required
def comment_update_view(request, slug, id):
	obj = get_object_or_404(Comment, id = id)
	form = CommentModelForm(request.POST or None, instance=obj)
	if form.is_valid():
		form.save()
		return redirect("/blog/"+slug)
	template_name = 'blog/form.html'

	context = {"form": form}
	return render(request,template_name,context)

@login_required
def comment_delete_view(request,slug, id):
	obj = get_object_or_404(Comment, id =id)
	template_name = 'blog/delete.html'
	if request.method == 'POST':
		obj.delete()
		return redirect("/blog/"+slug)
	context = {"object":obj}
	return render(request,template_name,context)


# def blog_post_create_view(request):
# 	form = BlogPostModelForm(request.POST or None)
	
# 	if form.is_valid():
# 		obj = BlogPost.objects.create(**form.cleaned_data)
# 		form = BlogPostForm()

# 	template_name = 'blog/form.html'
# 	context = {"form":form,}
# 	# return render(request,template_name,context)


# def blog_post_detail_page(request,slug):
# 	# obj = BlogPost.objects.get(pk = id)
# 	# obj = BlogPost.objects.get(slug = slug)
# 	# querrySet = BlogPost.objects.filter(slug = slug) return all values with slug

# 	# obj = get_object_or_404(BlogPost, slug = slug)

# 	# querrySet = BlogPost.objects.filter(slug = slug)

# 	# if querrySet.count() < 1:
# 	# 	raise Http404

# 	obj = get_object_or_404(BlogPost, slug = slug)

# 	template_name = 'blog_post_detail.html'
# 	context = {"object":obj}
# 	return render(request,template_name,context)


	# try:
	# 	obj = BlogPost.objects.get(id=post_id)
	# except BlogPost.DoesNotExist:
	# 	raise Http404
	# except ValueError:
	# 	raise Http404