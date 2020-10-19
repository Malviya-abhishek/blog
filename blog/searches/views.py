from django.shortcuts import render
from .models import SearchQuery
from django.contrib import messages

from blog.models import BlogPost
# Create your views here.

def search_view(request):
	query = request.GET.get('q', None)
	user = None
	if request.user.is_authenticated:
		user = request.user
	context = {"query":query}
	if query is not None:
		SearchQuery.objects.create(user=user, query=query)
		if len(query) > 0:
			messages.info(request, f"You searched for  { query } ")
		blog_list = BlogPost.objects.search(query=query)
		context['blog_list'] = blog_list

	return render(request, 'searches/view.html',context)