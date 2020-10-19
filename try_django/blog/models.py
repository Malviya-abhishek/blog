from django.db import models
from django.utils import timezone
#  this is used to connect user to a blog
from django.conf import settings
from django.db.models import Q
User = settings.AUTH_USER_MODEL


class BlogPostQuerySet(models.QuerySet):
	def published(self):
		now = timezone.now()
		return self.filter(publish_date__lte=now)

	def search(self, query):
		lookup = (
					Q(title__icontains=query)|
					Q(content__icontains=query)|
					Q(slug__icontains=query)|
					Q(user__first_name__icontains=query)|
					Q(user__last_name__icontains=query)|
					Q(user__username__icontains=query)
				)
		return 	self.filter(lookup)

class BlogPostManager(models.Manager):
	def get_queryset(self):
		return BlogPostQuerySet(self.model, using=self._db)

	def published(self):
		return self.get_queryset().published()

	def search(self, query=None):
		if query is None:
			return self .get_queryset().none()
		return self.get_queryset().published().search(query)


# class BlogPostManager(models.Manager):
# 	def published(self):
# 		now = timezone.now()
# 		return self.get_queryset().filter(publish_date__lte=now)

class BlogPost(models.Model):
	user = models.ForeignKey(User, default=1,null=True, on_delete= models.SET_NULL)
	title = models.CharField(max_length= 120 )
	slug = models.SlugField(unique= True)
	# the purpose of using a slug is to use beautifull urls
	content = models.TextField(null = True, blank=True)
	publish_date = models.DateTimeField(auto_now=False, auto_now_add=False,null=True,blank=True)
	timestamp = models.DateTimeField(auto_now_add=True) # time when data enter into system publish date can be changed by admin
	updated = models.DateTimeField(auto_now=True) # as its name it will change every time you update it
	# image = models.FileField(upload_to='image/', null=True, blank=True)
	image = models.ImageField(upload_to='image/', null=True, blank=True)
	objects = BlogPostManager()
	#uploadoing a file

	def __str__(self):
		return self.title


	class Meta:
		ordering = ['-publish_date', '-updated', '-timestamp'] # - is denoting recent first

	def get_absolute_url(self):
		return f"/blog/{self.slug}"

	def get_edit_url(self):
		return f"{self.get_absolute_url()}/edit"

	def get_delete_url(self):
		return f"{self.get_absolute_url()}/delete"


class Comment(models.Model):
	blog = models.ForeignKey(BlogPost,default=1,on_delete=models.CASCADE)
	user = models.ForeignKey(User, default=1,null=True, on_delete= models.SET_NULL)
	content= models.CharField(max_length=500)

	def __str__(self):
		return (str(self.user))
# class ClassName(models.Model):
# 	"""docstring for ClassName"""
# 	def __init__(self, arg):
# 		super(ClassName, self).__init__()
# 		self.arg = arg
		
# to importing user in powershell
# we use 
#from django.contrib.auth import get_user_model
# j = User.object.first()
# j.blogpost_set.all()
# the above line is lowercase class name _set 
# will look up for all the post made by first user