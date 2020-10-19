from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
# from django.conf import settings
# from django.db.model

class ContactForm(forms.Form):
	full_name = forms.CharField()
	email = forms.EmailField()
	content = forms.CharField(widget=forms.Textarea)

	def clean_email(self, *args, **kwargs): # this is a proper method and to named like this only

		email = self.cleaned_data.get('email')

		print(email)

		if email.endswith(".edu"):
			raise forms.ValidationError("do not use .edu")
		return email


class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ["username", "email", "password1", "password2"]

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user
