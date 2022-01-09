import datetime

from django import forms
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner', null=True) 
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.title


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description']

    
    def clean(self):
        super(forms.ModelForm, self).clean()

        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')

        if title == '':
            self._erros['title'] = self.error_class(['Preencha com o título do livro'])
        if description == '':
            self._erros['description'] = self.error_class(['Preencha com a descrição do livro'])

        return self.cleaned_data

class EditBookForm(forms.ModelForm):
    class Meta:
        model = Book 
        fields = ['title', 'description']


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user
