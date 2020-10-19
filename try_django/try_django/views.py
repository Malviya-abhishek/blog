from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.template.loader import get_template
from .form import ContactForm, NewUserForm
from blog.models import BlogPost
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

def home_page(request):
	qs = BlogPost.objects.all()[:5]
	context = {
				"title":"Welcome to django",
				 "blog_list":qs,
				}
	return render(request, "home.html", context)


def about_page(request):
	return render(request, "about_page.html", {})


def contact_page(request):
	form = ContactForm(request.POST or None)

	if form.is_valid():
		# print(form.cleaned_data)
		form = ContactForm()
		
	context = {
		'title': "contact page",
		"form": form,
	}

	return render(request, "form.html", context)

def logout_request(request):
	logout(request)
	messages.info(request, f"You are logged out succesfully")
	return redirect('/')


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    print('error')
    context={"form":form}
    template="login.html"
    return render(request,template,context)


def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			login(request, user)
			messages.info(request, f"You are now logged in as {username}")
			return redirect('/')
		else:
			messages.error(request, "Invalid password.")
			print("worng form")

	form = NewUserForm()
	print('error')
	template = "register.html"
	context = {"form":form}
	return render(request,template,context)

# def register(request):
# 	if request.method == "POST":
# 		form = NewUserForm(request.POST)
# 		if form.is_valid():
# 			user = form.save()
# 			username = form.cleaned_data.get('username')
# 			login(request, user)
# 			return redirect('/')
# 			username = form.cleaned_data.get('username')
# 			password = form.cleaned_data.get('password')
# 			userp = authenticate(request,username=username,password=password)
# 			if userp is not None:
# 				login(request,userp)
# 				messages.info(request, f"You are logged in as {username}")
# 				return redirect('/')

# 	form = NewUserForm()
# 	template = "register.html"
# 	context = {"form":form}
# 	return render(request,template,context)


# def contact_page(request):
# 	context = {'title': "contact page"}
# 	template_name = "contact_page.html"
# 	template_obj = get_template(template_name)
# 	return HttpResponse(template_obj.render(context))

