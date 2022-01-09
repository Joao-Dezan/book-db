from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import (
    Book, BookForm, EditBookForm, UserLoginForm, UserRegisterForm
)


@login_required()
def create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            return redirect('list')
        else:
            print(form.errors)
            return render(request, 'create_book.html', {'form': form})
    else:
        form = BookForm()
        return render(request, 'create_book.html', {'form': form})

@login_required()
def list(request):
    user = request.user
    books = Book.objects.filter(owner=user)
    return render(request, 'list_book.html', {'books': books})

@login_required()
def details(request, id=None):
    if id is not None:
        book = Book.objects.get(id=id)
        return render(request, 'details_book.html', {'book': book})
    else:
        HttpResponse('Invalid book id')

@login_required()
def edit(request, id=None):
    if request.method == 'POST':
        form = EditBookForm(request.POST)
        if form.is_valid():
            book = Book.objects.get(id=id)
            book.title = request.POST.get('title')
            book.description = request.POST.get('description')
            book.save()
            return redirect('list')
        else:
            print(form.errors)
            return render(request, 'edit_book.html', {'form': form})
    else:
        if id is not None:
            form = EditBookForm()
            book = Book.objects.get(id=id)
            return render(request, 'edit_book.html', {'form': form, 'book': book})

@login_required()
def delete(request, id=None):
    if id is not None:
        try:
            book = Book.objects.get(id=id)
            Book.delete(book)
        except:
            return HttpResponse('Unknown Error')
        else:
            return redirect('list')
    else:
        HttpResponse('Invalid book id')


@login_required()
def logout_view(request):
    logout(request)
    return redirect('login')

class SignUpView(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
